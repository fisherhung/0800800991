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

# ==========================================================
# ⚠️ 路徑設定說明：
# Windows 範例: "C:/Users/你的用戶名/Desktop/花蓮/腳本/"
# Mac 範例: "~/Desktop/花蓮/腳本/"
# ==========================================================
CUSTOM_OUTPUT_PATH = "~/Desktop/花蓮/腳本/" 
# ==========================================================

# 自動轉換路徑符號，確保 Win/Mac 都能讀懂
output_folder = os.path.abspath(os.path.expanduser(CUSTOM_OUTPUT_PATH))

def sanitize_filename(name):
    """清理檔名，避免 Win/Mac 不合法的字元"""
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def export_final_fixed():
    try:
        # 建立資料夾
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 取得目前圖層
        layer = iface.activeLayer()
        if not layer:
            print("❌ 錯誤：請先在圖層面板點選（反白）一個圖層！")
            return

        # --- 座標處理：強制轉換為 EPSG:3826 (TWD97) ---
        target_crs = QgsCoordinateReferenceSystem("EPSG:3826")
        source_crs = layer.crs()
        transform = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
        
        # 取得範圍並轉換座標
        original_extent = layer.extent()
        twd97_extent = transform.transformBoundingBox(original_extent)

        # --- 檔案命名 (圖層名 + 時間) ---
        clean_name = sanitize_filename(layer.name())
        timestamp = datetime.now().strftime("%H%M%S")
        filename_base = f"{clean_name}_{timestamp}"

        # --- 解析度與容量優化 (最大邊長 1280px) ---
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
        settings.setBackgroundColor(QColor(0, 0, 0, 0)) # 透明背景
        settings.setOutputSize(QSize(out_w, out_h))
        settings.setDestinationCrs(source_crs)

        # 啟動渲染任務
        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        
        image = job.renderedImage()
        if not image.isNull():
            # --- 極限容量優化：轉換為 8 位元索引色 (大幅縮小 PNG 大小) ---
            indexed_image = image.convertToFormat(QImage.Format_Indexed8)
            
            png_name = f"{filename_base}.png"
            png_path = os.path.join(output_folder, png_name)
            indexed_image.save(png_path, "PNG", 9) 

            # --- 準備符合系統規範的 JSON 資料 ---
            data = {
                "name": layer.name(),
                "n": twd97_extent.yMaximum(),
                "s": twd97_extent.yMinimum(),
                "w": twd97_extent.xMinimum(),
                "e": twd97_extent.xMaximum(),
                "crs": "EPSG:3826",
                "description": "Exported with 3826 Forced Fix",
                "file_ref": png_name
            }

            json_name = f"{filename_base}.json"
            json_path = os.path.join(output_folder, json_name)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # 顯示輸出結果
            file_size_kb = os.path.getsize(png_path) / 1024
            print("-" * 30)
            print(f"✅ 匯出完成 (跨平台相容)")
            print(f"📄 JSON: {json_name}")
            print(f"🖼️  PNG : {png_name} ({file_size_kb:.1f} KB)")
            print(f"📍 座標系: EPSG:3826")
            print(f"📂 路徑: {output_folder}")
            print("-" * 30)
        else:
            print("❌ 錯誤：影像渲染失敗。")

    except Exception as e:
        print(f"❌ 發生錯誤: {str(e)}")

# 執行
export_final_fixed()
