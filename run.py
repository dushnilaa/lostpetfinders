from parser import Parser


if __name__ == '__main__':
    parser = Parser()
    search_result = parser.download_json()
    parser.write_db(search_result)
    parser.update_pages()
