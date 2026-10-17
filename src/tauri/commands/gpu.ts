import { core } from '@tauri-apps/api'

import { GpuInfo } from '@/types/compression'

export function getGpuInfo(): Promise<GpuInfo> {
  return core.invoke('get_gpu_info_command')
}
