import { useCallback, useEffect, useState } from 'react'
import { useSnapshot } from 'valtio'

import Switch from '@/components/Switch'
import Tooltip from '@/components/Tooltip'
import Icon from '@/components/Icon'
import { getGpuInfo } from '@/tauri/commands/gpu'
import { GpuInfo } from '@/types/compression'
import { appProxy, normalizeBatchMediaConfig } from '../../../../-state'

type GpuAccelerationProps = {
  mediaIndex: number
}

function GpuAcceleration({ mediaIndex }: GpuAccelerationProps) {
  const {
    state: {
      media,
      isCompressing,
      isProcessCompleted,
      commonConfigForBatchCompression,
      isLoadingMediaFiles,
    },
  } = useSnapshot(appProxy)

  const [gpuInfo, setGpuInfo] = useState<GpuInfo | null>(null)

  useEffect(() => {
    let isMounted = true
    getGpuInfo()
      .then((info) => {
        if (isMounted) {
          setGpuInfo(info)
        }
      })
      .catch((err) => {
        console.error('Failed to get GPU info:', err)
      })
    return () => {
      isMounted = false
    }
  }, [])

  const video =
    media.length > 0 && mediaIndex >= 0 && media[mediaIndex].type === 'video'
      ? media[mediaIndex]
      : null

  const { config } = video ?? {}
  const enableGpu =
    (config ?? commonConfigForBatchCompression.videoConfig)?.enableGpu ?? true

  const handleToggle = useCallback(() => {
    const nextVal = !enableGpu
    if (
      mediaIndex >= 0 &&
      appProxy.state.media[mediaIndex]?.type === 'video' &&
      appProxy.state.media[mediaIndex]?.config
    ) {
      appProxy.state.media[mediaIndex].config.enableGpu = nextVal
      appProxy.state.media[mediaIndex].isConfigDirty = true
    } else {
      if (appProxy.state.media.length > 1) {
        appProxy.state.commonConfigForBatchCompression.videoConfig.enableGpu = nextVal
        normalizeBatchMediaConfig()
      }
    }
  }, [enableGpu, mediaIndex])

  const shouldDisableInput =
    media.length === 0 ||
    isCompressing ||
    isProcessCompleted ||
    isLoadingMediaFiles

  const isNvidia = gpuInfo?.isNvidia ?? true

  return (
    <div className="flex flex-col gap-2 p-2 rounded-xl bg-content2/40 border border-content3/60">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-sm font-medium text-foreground">
            GPU Acceleration (NVENC)
          </span>
          <Tooltip
            content="Accelerates video encoding using your NVIDIA GPU hardware chips (NVENC) for dramatic speed increases."
            aria-label="GPU Acceleration info"
          >
            <Icon
              name="info"
              className="inline-block text-primary cursor-pointer"
              size={14}
            />
          </Tooltip>
        </div>

        <Switch
          isSelected={enableGpu && isNvidia}
          onValueChange={handleToggle}
          isDisabled={shouldDisableInput || !isNvidia}
          size="sm"
        />
      </div>

      <div className="flex items-center justify-between text-xs text-default-500">
        <span className="flex items-center gap-1">
          <span
            className={`inline-block w-2 h-2 rounded-full ${
              enableGpu && isNvidia ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
            }`}
          />
          {gpuInfo ? gpuInfo.gpuName : 'Detecting NVIDIA GPU...'}
        </span>
        {enableGpu && isNvidia ? (
          <span className="text-[10px] font-semibold text-emerald-500 dark:text-emerald-400 uppercase tracking-wider bg-emerald-500/10 px-1.5 py-0.5 rounded">
            GPU Active
          </span>
        ) : (
          <span className="text-[10px] text-default-400 uppercase tracking-wider bg-default-500/10 px-1.5 py-0.5 rounded">
            CPU Mode
          </span>
        )}
      </div>
    </div>
  )
}

export default GpuAcceleration
