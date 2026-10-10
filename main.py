import csv
import json
import argparse


def file_reader(input_file):
    if input_file.endswith('.csv'):
        return csv_reader(input_file)
    elif input_file.endswith('.json'):
        return json_reader(input_file)
    else:
        raise ValueError("Тип файла не поддерживается")


def csv_reader(input_file):
    with open(input_file, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)

        data = [dict(row) for row in reader]

        return data


def json_reader(input_file):
    with open(input_file, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        return data


def validate(data):
    for row in data:
        if 'id' not in row or 'text' not in row:
            return "Error"

        row['id'] = str(row['id']).strip()
        row['text'] = str(row['text']).strip().replace('ё', 'е')

        if not row['id'] or not row['text']:
            return "Error"
    return data


def write_json(result, output_file):
    try:
        with open(output_file, mode='r', encoding='utf-8') as file:
            existing_results = json.load(file)
    except FileNotFoundError:
        existing_results = []

    existing_ids = {res['id']: i for i, res in enumerate(existing_results)}

    for row in result:
        if row['id'] in existing_ids:
            existing_results[existing_ids[row['id']]] = row
        else:
            existing_results.append(row)
            existing_ids[row['id']] = len(existing_results) - 1

    with open(output_file, mode='w', encoding='utf-8') as file:
        json.dump(existing_results, file, ensure_ascii=False, indent=4)

    return output_file


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='Path to the input file'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        required=True,
        help='Path to the output JSON file'
    )

    args = parser.parse_args()

    try:
        data = file_reader(args.input)
    except FileNotFoundError:
        print("Ошибка: входной файл не найден")
        return 1
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON")
        return 1
    except ValueError as e:
        print(e)
        return 1

    data = validate(data)

    if data == 'Error':
        print("Ошибка: отсутствует или пусто поле id или text")
        return 1

    result = []

    write_json(result, args.output)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
