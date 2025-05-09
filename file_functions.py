# Funkcja do formatowania rozmiaru pliku na czytelną postać (np. KB, MB, GB)
def format_size(size_mb):
    size = size_mb * 1024 * 1024 
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    # Przeliczanie rozmiaru na odpowiednią jednostkę
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"
