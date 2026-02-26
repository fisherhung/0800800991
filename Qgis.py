import json
import os
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QImage

# --- 自定義路徑設定 ---
# 針對 Mac 環境，確保路徑正確
output_folder = os.path.abspath("/Users/hung/Desktop/花蓮/腳本/")

try:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 取得目前選取的圖層
    layer = iface.activeLayer()
    if not layer:
        print("❌ 錯誤：請先在左側圖層面板中點選（反白）一個圖層！")
    else:
        # 確保獲取的是圖層的範圍
        extent = layer.extent()
        crs_authid = layer.crs().authid()

        # 1. 準備座標中繼資料 (JSON)
        data = {
            "name": layer.name(),
            "n": extent.yMaximum(),
            "s": extent.yMinimum(),
            "w": extent.xMinimum(),
            "e": extent.xMaximum(),
            "crs": crs_authid,
            "description": "Exported from Hualien Project"
        }

        # 匯出 JSON 檔案
        json_path = os.path.join(output_folder, "map_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        # 2. 準備影像繪製設定
        settings = QgsMapSettings()
        settings.setLayers([layer])
        settings.setExtent(extent)
        settings.setOutputDpi(96)
        settings.setBackgroundColor(QColor(0, 0, 0, 0)) # 透明背景
        
        # 設定影像大小 (2048x2048)
        settings.setOutputSize(QSize(2048, 2048)) 

        # 3. 執行渲染任務
        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()
        
        # 取得渲染完成的影像並儲存
        image = job.renderedImage()
        if not image.isNull():
            image_path = os.path.join(output_folder, "map_overlay.png")
            image.save(image_path, "PNG")

            print("-" * 30)
            print(f"✅ 匯出成功！已儲存至：{output_folder}")
            print(f"📄 設定檔: map_data.json")
            print(f"🖼️ 影像檔: map_overlay.png")
            print("-" * 30)
        else:
            print("❌ 錯誤：影像渲染失敗，產出的影像為空。")

except Exception as e:
    print(f"❌ 發生非預期錯誤: {str(e)}")