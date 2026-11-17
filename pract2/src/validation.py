from pathlib import Path
from urllib.parse import urlparse

def validate_args(args, parser):
    #Проверка ошибок
    if not args.package.strip():
        parser.error("Имя пакета не должно быть пустым")
    if not args.version.strip():
        parser.error("Название версии не должно быть пустым")
    if not args.repository.strip():
        parser.error("Имя репозитория не должно быть пустым")

    output_path = Path(args.output)
    if output_path.suffix != ".svg" or not output_path.stem.strip():
        parser.error("Укажите имя файла с расширением .svg")

    if args.test:
        if not Path(args.repository).is_file():
            parser.error("Файл тестового репозитория не найден")
    else:
        try:
            url = urlparse(args.repository)
        except ValueError:
            parser.error("Некорректный URL репозитория")
        if url.scheme not in ("http", "https") or not url.netloc:
            parser.error("Укажите URL репозитория с протоколом http или https")