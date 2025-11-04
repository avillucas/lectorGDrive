# File Renaming Script

Bash script to rename files based on JSON data from Google Drive.

## Usage

```bash
# Make script executable
chmod +x rename_files.sh

# Run in dry-run mode (default)
./rename_files.sh

# Run for real (actually copy/rename files)
DRY_RUN=false ./rename_files.sh
```

## Requirements

- `jq` - JSON processor
- `bash` 4.0 or higher

Install jq on Ubuntu/Debian:
```bash
sudo apt install jq
```

## What it does

1. Reads `/home/lucas/divit/lectorGDrive/salida/salida.talleres.json`
2. For each object:
   - Takes the `file` attribute
   - Removes "articulos - " prefix if present
   - Changes .txt extension to .pdf
   - Searches for matching file in `talleres e.e.` directory
   - Copies file to `talleres_back` with name from `title` attribute + .pdf extension

## Features

- **Dry-run mode** by default - shows what would happen without making changes
- **Fuzzy matching** - finds files even if names don't match exactly
- **Filename sanitization** - removes invalid characters from titles
- **Progress tracking** - shows current item being processed
- **Detailed logging** - color-coded output for easy reading
- **Error handling** - continues processing even if individual files fail

## Example

JSON entry:
```json
{
  "file": "articulos - 2009-03-04_El_Plan_de_Dios_en_Pablo_e_Ignacio.txt",
  "title": "El Plan de Dios en Pablo e Ignacio"
}
```

Will look for: `2009-03-04_El_Plan_de_Dios_en_Pablo_e_Ignacio.pdf`
And rename to: `El Plan de Dios en Pablo e Ignacio.pdf`
