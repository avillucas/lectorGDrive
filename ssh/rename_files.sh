#!/bin/bash
# filepath: /home/lucas/divit/lectorGDrive/ssh/rename_files.sh

# Script to rename files based on JSON data
# Reads salida.talleres.json and renames files from 'talleres e.e.' directory

set -e  # Exit on error

# Configuration
JSON_FILE="/home/lucas/divit/lectorGDrive/salida/salida.talleres.json"
SOURCE_DIR="/home/lucas/divit/lectorGDrive/salida/talleres e.e."
DEST_DIR="/home/lucas/divit/lectorGDrive/salida/talleres_back"
DRY_RUN=${DRY_RUN:-true}  # Set to 'false' to actually rename files

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to sanitize filename (remove invalid characters)
sanitize_filename() {
    local filename="$1"
    # Remove or replace invalid characters for filenames
    echo "$filename" | sed 's/[<>:"/\\|?*]//g' | sed 's/  */ /g' | sed 's/^ *//;s/ *$//'
}

# Function to extract filename from JSON file attribute
extract_filename() {
    local file_attr="$1"
    # Remove "articulos - " prefix if it exists and change .txt to .pdf
    echo "$file_attr" | sed 's/^articulos - //' | sed 's/\.txt$/.pdf/'
}

# Function to find matching file in source directory
find_matching_file() {
    local search_name="$1"
    local source_dir="$2"
    
    # Remove extension to get base name
    local base_name=$(basename "$search_name" .pdf)
    
    # Look for exact match first
    if [[ -f "$source_dir/$search_name" ]]; then
        echo "$source_dir/$search_name"
        return 0
    fi
    
    # Look for file with same base name but any extension
    for file in "$source_dir"/*; do
        if [[ -f "$file" ]]; then
            local file_base=$(basename "$file" | sed 's/\.[^.]*$//')
            if [[ "$file_base" == "$base_name" ]]; then
                echo "$file"
                return 0
            fi
        fi
    done
    
    # Fuzzy search - look for files containing key parts
    local date_part=$(echo "$base_name" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}')
    if [[ -n "$date_part" ]]; then
        for file in "$source_dir"/*"$date_part"*; do
            if [[ -f "$file" ]]; then
                echo "$file"
                return 0
            fi
        done
    fi
    
    return 1
}

# Function to rename/copy file
rename_file() {
    local source_file="$1"
    local new_title="$2"
    local dest_dir="$3"
    local dry_run="$4"
    
    # Get original extension
    local extension="${source_file##*.}"
    
    # Sanitize new title
    local sanitized_title=$(sanitize_filename "$new_title")
    
    # Create new filename
    local new_filename="${sanitized_title}.${extension}"
    local dest_path="$dest_dir/$new_filename"
    
    if [[ "$dry_run" == "true" ]]; then
        log_info "[DRY RUN] Would copy: '$(basename "$source_file")' -> '$new_filename'"
        return 0
    fi
    
    # Create destination directory if it doesn't exist
    mkdir -p "$dest_dir"
    
    # Check if destination file already exists
    if [[ -f "$dest_path" ]]; then
        log_warning "Destination file already exists: '$new_filename' - skipping"
        return 1
    fi
    
    # Copy file with new name
    if cp "$source_file" "$dest_path"; then
        log_success "Copied: '$(basename "$source_file")' -> '$new_filename'"
        return 0
    else
        log_error "Failed to copy file: $source_file"
        return 1
    fi
}

# Main script
main() {
    log_info "Starting file renaming script"
    log_info "JSON file: $JSON_FILE"
    log_info "Source directory: $SOURCE_DIR"
    log_info "Destination directory: $DEST_DIR"
    log_info "Dry run mode: $DRY_RUN"
    
    # Check if JSON file exists
    if [[ ! -f "$JSON_FILE" ]]; then
        log_error "JSON file not found: $JSON_FILE"
        exit 1
    fi
    
    # Check if source directory exists
    if [[ ! -d "$SOURCE_DIR" ]]; then
        log_error "Source directory not found: $SOURCE_DIR"
        exit 1
    fi
    
    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed. Please install jq first."
        exit 1
    fi
    
    # Count total items
    local total_items=$(jq '. | length' "$JSON_FILE")
    log_info "Found $total_items items to process"
    
    # Counters
    local processed=0
    local successful=0
    local failed=0
    local not_found=0
    
    # Process each item in JSON
    while IFS= read -r item; do
        processed=$((processed + 1))
        
        # Extract fields from JSON object
        local file_attr=$(echo "$item" | jq -r '.file // empty')
        local title=$(echo "$item" | jq -r '.title // empty')
        
        echo ""
        log_info "Processing $processed/$total_items"
        
        # Skip if missing required fields
        if [[ -z "$file_attr" || -z "$title" ]]; then
            log_warning "Skipping item - missing file or title"
            failed=$((failed + 1))
            continue
        fi
        
        # Extract filename and convert .txt to .pdf
        local search_filename=$(extract_filename "$file_attr")
        log_info "Looking for file: $search_filename"
        
        # Find matching file in source directory
        local source_file
        if source_file=$(find_matching_file "$search_filename" "$SOURCE_DIR"); then
            log_info "Found file: $(basename "$source_file")"
            
            # Rename/copy the file
            if rename_file "$source_file" "$title" "$DEST_DIR" "$DRY_RUN"; then
                successful=$((successful + 1))
            else
                failed=$((failed + 1))
            fi
        else
            log_warning "File not found: $search_filename"
            not_found=$((not_found + 1))
            
            # Show some similar files for debugging
            log_info "Files in source directory matching pattern:"
            find "$SOURCE_DIR" -name "*$(echo "$search_filename" | cut -d'_' -f1)*" -type f | head -3 | while read -r similar_file; do
                log_info "  Similar: $(basename "$similar_file")"
            done
        fi
    done < <(jq -c '.[]' "$JSON_FILE")
    
    # Final summary
    echo ""
    log_info "============================================================"
    log_info "FINAL SUMMARY:"
    log_info "Total items processed: $processed"
    log_success "Successfully copied: $successful"
    log_error "Failed: $failed"
    log_warning "Not found: $not_found"
    
    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "NOTE: This was a dry run - no files were actually copied"
        log_info "Set DRY_RUN=false to perform actual file operations"
    else
        log_info "Files copied to: $DEST_DIR"
    fi
    log_info "============================================================"
}

# Run main function
main "$@"