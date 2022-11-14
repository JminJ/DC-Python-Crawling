# DC-Python-Crawling
## Intro
Dcincide 중 국내야구갤러리에서 특정 키워드를 검색 후 키워드가 포함된 글 제목들을 추출하는 크롤러입니다.
## How to use?
```bash
python src/dc_keyword_crawling.py \
    --keword=KEYWORD \
    --extract_range=10 \
    --base_save_dir_path=BASE_SAVE_DIR_PATH \
    --user_agent=USER_AGENT \
```
```
Note) user_agent를 확인하는 방법은 하단에서 확인하실 수 있습니다.
```
## Parameter
| parameter | type | description | default |
| ---------- | ---------- | ---------- | --------- |
| keyword | str | 추출 할 키워드를 지정합니다. | - |
| extract_range | int | 글의 제목을 추출할 총 페이지 수 입니다. | 10 |
| base_save_dir_path | str | dataframe이 저장될 디렉토리 경로입니다. | - |
| user_agent | str | 본인의 user_agent입니다. | None |

## How to get User-Agent?
* [whatsmyua 사이트](https://www.whatsmyua.info/)
