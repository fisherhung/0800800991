import json
import os
import re
from datetime import datetime
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QImage
from qgis.core import (
    QgsMapSettings, 
    QgsMapRendererSequentialJob, 
    QgsCoordinateReferenceSystem, 
    QgsCoordinateTransform,
    QgsProject
)

# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
output_folder = os.path.expanduser("~/Desktop/花蓮/腳本/")
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
# --- 設定匯出資料夾 ---
def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def export_final_fixed():
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        layer = iface.activeLayer()
        if not layer:
            print("❌ 錯誤：請先點選一個圖層！")
            return

        # --- 座標處理：強制轉為 EPSG:3826 ---
        target_crs = QgsCoordinateReferenceSystem("EPSG:3826")
        source_crs = layer.crs()
        transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
        
        # 取得強制轉換後的範圍
        original_extent = layer.extent()
        twd97_extent = transform.transformBoundingBox(original_extent)

        # --- 檔案命名 ---
        clean_name = sanitize_filename(layer.name())
        timestamp = datetime.now().strftime("%H%M%S")
        filename_base = f"{clean_name}_{timestamp}"

        # --- 容量優化：設定尺寸 (最大邊 1280px 已足夠協作系統使用) ---
        max_dim = 1280 
        width = original_extent.width()
        height = original_extent.height()
        
        if width > height:
            out_w = max_dim
            out_h = int(max_dim * (height / width))
        else:
            out_h = max_dim
            out_w = int(max_dim * (width / height))

        # --- 渲染設定 ---
        settings = QgsMapSettings()
        settings.setLayers([layer])
        settings.setExtent(original_extent)
        settings.setOutputDpi(72)
        settings.setBackgroundColor(QColor(0, 0, 0, 0))
        settings.setOutputSize(QSize(out_w, out_h))
        settings.setDestinationCrs(source_crs)

        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        
        image = job.renderedImage()
        if not image.isNull():
            # --- 極限容量優化：轉換為 8位元索引色 (大幅縮減體積) ---
            indexed_image = image.convertToFormat(QImage.Format_Indexed8)
            
            png_path = os.path.join(output_folder, f"{filename_base}.png")
            # 使用最高壓縮級別 (9)
            indexed_image.save(png_path, "PNG", 9) 

            # --- 準備 JSON 資料 (固定輸出 EPSG:3826) ---
            data = {
                "name": layer.name(),
                "n": twd97_extent.yMaximum(),
                "s": twd97_extent.yMinimum(),
                "w": twd97_extent.xMinimum(),
                "e": twd97_extent.xMaximum(),
                "crs": "EPSG:3826", # 強制標記為 3826
                "description": "Exported with 3826 Forced Fix"
            }

            json_path = os.path.join(output_folder, f"{filename_base}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            file_size_kb = os.path.getsize(png_path) / 1024
            print("-" * 30)
            print(f"✅ 強制 3826 匯出成功！")
            print(f"📄 JSON: {os.path.basename(json_path)}")
            print(f"🖼️  PNG: {os.path.basename(png_path)} ({file_size_kb:.1f} KB)")
            print(f"📍 座標已強制修正為: EPSG:3826")
            print("-" * 30)
        else:
            print("❌ 錯誤：影像渲染失敗。")

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")

export_final_fixed()
