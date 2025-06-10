#!/bin/bash

# Dataset extraction script (cleaned structure)
# Extract UCF-Crime and XD-Violence datasets to appropriate locations

echo "=== Starting dataset extraction ==="

# === XD-Violence ===
echo "Extracting XD-Violence dataset..."

mkdir -p "src/videos/xd-violence/videos/train"
mkdir -p "src/videos/xd-violence/videos/test"

# train: 1.zip ~ 5.zip → train/ 
for i in {1..5}; do
    if [ -f "${i}.zip" ]; then
        echo "  Extracting ${i}.zip into train/..."
        unzip -q "${i}.zip" -d "src/videos/xd-violence/videos/train/"
        echo "  ${i}.zip completed"
    else
        echo "  Warning: ${i}.zip not found"
    fi
done

# test.zip → test/ 
if [ -f "test.zip" ]; then
    echo "  Extracting test.zip into test/..."
    unzip -q "test.zip" -d "src/videos/xd-violence/videos/"
    echo "  test.zip completed"
    
    echo "  Organizing XD-Violence test videos..."
    # Move videos from extracted videos folder to test folder directly
    if [ -d "src/videos/xd-violence/videos/videos" ]; then
        mv "src/videos/xd-violence/videos/videos"/*.* "src/videos/xd-violence/videos/test/" 2>/dev/null
        # Clean up empty videos folder
        rm -rf "src/videos/xd-violence/videos/videos"
        echo "  XD-Violence test organization completed"
    fi
else
    echo "  Warning: test.zip not found"
fi

# === UCF-Crime ===
echo "Extracting UCF-Crime dataset..."

mkdir -p "src/videos/ucf-crime/videos/train"
mkdir -p "src/videos/ucf-crime/videos/test"

if [ -f "UCF_Crimes.zip" ]; then
    echo "  Extracting UCF_Crimes.zip..."
    unzip -q "UCF_Crimes.zip" -d "src/videos/ucf-crime/videos/"
    echo "  UCF_Crimes.zip completed"
    
    echo "  Organizing UCF-Crime videos..."
    
    # Check if split files exist
    TRAIN_FILE="src/videos/ucf-crime/videos/UCF_Crimes/Anomaly_Detection_splits/Anomaly_Train.txt"
    TEST_FILE="src/videos/ucf-crime/videos/UCF_Crimes/Anomaly_Detection_splits/Anomaly_Test.txt"
    
    if [ -f "$TRAIN_FILE" ] && [ -f "$TEST_FILE" ]; then
        echo "    Using official train/test splits..."
        
        # Move training videos based on Anomaly_Train.txt
        while IFS= read -r line; do
            if [ ! -z "$line" ]; then
                video_path="src/videos/ucf-crime/videos/UCF_Crimes/Videos/$line"
                if [ -f "$video_path" ]; then
                    echo "    Moving $(basename "$line") to train/"
                    mv "$video_path" "src/videos/ucf-crime/videos/train/" 2>/dev/null
                fi
            fi
        done < "$TRAIN_FILE"
        
        # Move testing videos based on Anomaly_Test.txt
        while IFS= read -r line; do
            if [ ! -z "$line" ]; then
                video_path="src/videos/ucf-crime/videos/UCF_Crimes/Videos/$line"
                if [ -f "$video_path" ]; then
                    echo "    Moving $(basename "$line") to test/"
                    mv "$video_path" "src/videos/ucf-crime/videos/test/" 2>/dev/null
                fi
            fi
        done < "$TEST_FILE"
        
    else
        echo "    Error: Split files not found!"
        exit 1
    fi
    
    # Clean up empty extracted folder structure
    rm -rf "src/videos/ucf-crime/videos/UCF_Crimes"
    
    echo "  UCF-Crime organization completed"
else
    echo "  Warning: UCF_Crimes.zip not found"
fi

echo ""
echo "=== All extraction tasks completed ==="