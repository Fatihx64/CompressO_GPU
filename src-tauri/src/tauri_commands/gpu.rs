use crate::sys::gpu::{get_gpu_info, GpuInfo};

#[tauri::command]
pub async fn get_gpu_info_command() -> Result<GpuInfo, String> {
    Ok(get_gpu_info())
}
