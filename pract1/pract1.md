# Практическая работа 1

## Задание 1
```bash
grep '^[^:]*' /etc/passwd | sort
```
![alt text](image-2.png)

## Задание 2
```bash
grep -v '^#' /etc/protocols | awk 'NF >= 2 {print $2, $1}' | sort -nr | head -5
```
![alt text](image-1.png)

## Задание 3
```bash
#!/bin/bash

text="$*"
length=${#text}

printf '+'
printf '%*s' "$((length + 2))" '' | tr ' ' '-'
printf '+\n'

printf '| %s |\n' "$text"

printf '+'
printf '%*s' "$((length + 2))" '' | tr ' ' '-'
printf '+\n'
```
![alt text](image-3.png)

## Задание 4
Содержимое файла hello.cpp:
```C++
#include <iostream>

int main() {
    std::cout << "Hello World!\n";
    return 0;
}
```
identifiers:
```bash
#!/bin/bash

grep -oE '[A-Za-z_][A-Za-z0-9_]*' "$1" | sort -u
```
![alt text](image-4.png)

## Задание 5
```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 program"
    exit 1
fi

program="$1"

if [ ! -f "$program" ]; then
    echo "File not found: $program"
    exit 1
fi

chmod +x "$program"
sudo cp "$program" /usr/local/bin/

echo "Program $(basename "$program") registered succesfully"
```
![alt text](image-5.png)

## Задание 6
```bash
#!/bin/bash

find . -type f \( -name "*.c" -o -name "*.js" -o name "*.py" \) | while IFS= read -r file
do
    first_line=$(head -n 1 "$file")

    case "$file" in
        *.py)
            if [[ "$first_line" == \#* ]]; then
                echo "$file: comment found"
            else
                echo "$file: no comment"
            fi
            ;;
        *.c|*.js)
            if [[ "$first_line" == //* || "first_line" == \/* ]]; then
                echo "$file: comment found"
            else
                echo "$file: no comment"
            fi
            ;;
    esac
done
```
![alt text](image-6.png)

## Задание 7
```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 directory"
    exit 1
fi

find "$1" -type f -exec shasum -a 256 {} \; |
    sort |
    awk '
    {
        hash = $1
        file = substr($0, index($0, $2))
        files[hash] = files[hash] "\n" file
        count[hash]++
    }
    END {
        for (hash in count) {
            if (count[hash] > 1) {
                print "Duplicates:"
                print files[hash]
                print ""
            }
        }
    }'
```
![alt text](image-7.png)

## Задание 8
```bash
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 directory extension"
    exit 1
fi

directory="$1"
extension="$2"
archive="archive.tar"

find "$directory" -type f -name "*.$extension" -print0 |
    tar --null -T - -cf "$archive"

echo "Created: $archive"
```
![alt text](image-8.png)

## Задание 9
Тестовый файл содержит следующее:
```
This is a test file. Shla    Sasha    po    shosse    i    sosala    sushku.
```
Программа:
```bash
#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 input_file output_file"
    exit 1
fi

sed 's/    /\t/g' "$1" > "$2"
```
![alt text](image-9.png)
Возможно, на скриншоте не заметно, но программа заменила необходимые пробелы на знак табуляции

## Задание 10
```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 directory"
    exit 1
fi

find "$1" -type f -size 0 \( \
    -name "*.txt" -o \
    -name "*.text" \
\) -print
```
Для тестирования я создал 3 пустых текстовых файла.
![alt text](image-10.png)
