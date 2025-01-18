#!/bin/bash

# Change to script directory
cd "$(dirname "$0")" || exit 1

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Audio files directory
AUDIO_DIR="audio"

# All common audio formats
declare -a FORMATS=(
    "mp3" "wav" "m4a" "ogg" "wma"  # Common formats
    "aac" "flac" "aiff" "m4b" "m4p" "m4r" "mp2" "mp4" "mpga" "oga" "mogg" "opus" "ra" "rm" "vox" "webm"  # Other formats
)

# Check for ffmpeg
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo -e "${RED}Error: ffmpeg is not installed!${NC}"
        echo -e "${YELLOW}Please install ffmpeg:${NC}"
        echo "brew install ffmpeg"
        echo -e "\nPress Enter to continue..."
        read
        exit 1
    fi
}

# Process audio files
process_audio_files() {
    local found_files=0
    local success_files=0
    
    echo -e "\n${GREEN}Searching for audio files in: ${AUDIO_DIR}...${NC}"
    
    # Find and process files for each format
    for format in "${FORMATS[@]}"; do
        while IFS= read -r -d '' file; do
            if [ -f "$file" ]; then
                ((found_files++))
                echo -e "\n${GREEN}Processing: ${file}${NC}"
                
                # Send to Python with TR language
                if python3 transcribe.py "$file" "TR"; then
                    ((success_files++))
                else
                    echo -e "${RED}Processing failed: ${file}${NC}"
                fi
            fi
        done < <(find "$AUDIO_DIR" -type f -iname "*.$format" -print0)
    done
    
    if [ $found_files -eq 0 ]; then
        echo -e "\n${RED}Error: No audio files found in ${AUDIO_DIR}!${NC}"
        echo -e "${YELLOW}Please copy your audio files to the '${AUDIO_DIR}' directory.${NC}"
        echo -e "${YELLOW}Supported formats: ${FORMATS[*]}${NC}"
        return 1
    else
        if [ $success_files -eq $found_files ]; then
            echo -e "\n${GREEN}All files processed successfully. Total: ${found_files}${NC}"
        else
            echo -e "\n${YELLOW}${success_files}/${found_files} files processed successfully.${NC}"
        fi
    fi
}

# Main program
main() {
    echo -e "${GREEN}Starting audio file transcription...${NC}"
    echo -e "${YELLOW}Supported formats: ${FORMATS[*]}${NC}"

    # Check for ffmpeg
    check_ffmpeg

    # Check directory
    if [ ! -d "$AUDIO_DIR" ]; then
        echo -e "${YELLOW}Creating audio files directory...${NC}"
        mkdir -p "$AUDIO_DIR"
    fi

    # Process files
    process_audio_files
}

# Run main program
main "$@"

# Done
echo -e "\n${GREEN}Process completed. Press Enter to exit...${NC}"
read -n 1
