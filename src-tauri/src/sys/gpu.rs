use serde::{Deserialize, Serialize};
use wgpu::{Backends, Instance};

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub enum GpuType {
    Nvidia,
    Amd,
    AppleSilicon,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
#[serde(rename_all = "camelCase")]
pub struct GpuInfo {
    pub has_gpu: bool,
    pub is_nvidia: bool,
    pub gpu_name: String,
    pub vendor_id: u32,
    pub supported_encoders: Vec<String>,
}

/// Detect GPU(if available) on the system.
pub fn detect_gpu() -> Option<GpuType> {
    let instance = Instance::default();
    let adapters = instance.enumerate_adapters(Backends::all());

    for adapter in adapters {
        let info = adapter.get_info();

        let gpu = match info.vendor {
            0x10DE => Some(GpuType::Nvidia),
            0x1002 | 0x1022 => Some(GpuType::Amd),
            0x106b => Some(GpuType::AppleSilicon),
            _ => None,
        };

        if gpu.is_some() {
            return gpu;
        }

        match info.device_type {
            wgpu::DeviceType::IntegratedGpu => {
                if info.name.contains("Apple") {
                    return Some(GpuType::AppleSilicon);
                }
            }
            wgpu::DeviceType::DiscreteGpu => {
                if info.name.contains("AMD") {
                    return Some(GpuType::Amd);
                }
            }
            _ => {}
        }
    }
    None
}

/// Returns detailed GPU information and supported hardware encoders.
pub fn get_gpu_info() -> GpuInfo {
    let instance = Instance::default();
    let adapters = instance.enumerate_adapters(Backends::all());

    for adapter in adapters {
        let info = adapter.get_info();
        if info.vendor == 0x10DE || info.name.to_lowercase().contains("nvidia") {
            let mut supported_encoders = vec!["h264_nvenc".to_string(), "hevc_nvenc".to_string()];
            let name_lower = info.name.to_lowercase();
            // RTX 40 and RTX 50 series (Ada Lovelace / Blackwell) support AV1 hardware encoding
            if name_lower.contains("rtx 40")
                || name_lower.contains("rtx 50")
                || name_lower.contains("ada")
            {
                supported_encoders.push("av1_nvenc".to_string());
            }

            return GpuInfo {
                has_gpu: true,
                is_nvidia: true,
                gpu_name: info.name,
                vendor_id: info.vendor,
                supported_encoders,
            };
        }
    }

    // Secondary scan: check any discrete GPU
    let instance = Instance::default();
    let adapters = instance.enumerate_adapters(Backends::all());
    for adapter in adapters {
        let info = adapter.get_info();
        if info.vendor != 0 {
            return GpuInfo {
                has_gpu: true,
                is_nvidia: false,
                gpu_name: info.name,
                vendor_id: info.vendor,
                supported_encoders: Vec::new(),
            };
        }
    }

    GpuInfo {
        has_gpu: false,
        is_nvidia: false,
        gpu_name: "No discrete GPU detected".to_string(),
        vendor_id: 0,
        supported_encoders: Vec::new(),
    }
}
