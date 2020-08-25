# wtagger

## wtagger apis

### api table

name|method|parameter|url|cur example
--|--|--|--|--
company-name-candi|GET|company_name|/api/\<lang\>/company-name-candi|curl "http://127.0.0.1:5000/api/ko/company-name-candi?company_name=round"
company-name-by-tag|GET|tag|/api/\<lang\>/company-name-by-tag|curl "http://127.0.0.1:5000/api/ko/company-name-by-tag?tag=round"
add-company-tag|PATCH|id / tag|/api/\<lang\>/add-company-tag|curl -X PATCH -d '{"id": 1, "tags":["마이태그1","마이태2"]} http://127.0.0.1:5000/api/ko/add-company-tag
remove-company-tag|PATCH|id / tags|/api/\<lang\>/add-company-tag|curl -X POST -d '{"id": 1, "tags":["마이태그1", "마이태그2"]} http://127.0.0.1:5000/api/ko/remove-company-tag
add-company|POST|- company_name_\*: (optional) <br/> - company_tag_\* : optional|/api/add-company|curl -X POST -d '{"company_name_ko":"소소", "company_tag_ko":"멋진\|이렇게"}' http://127.0.0.1:5000/api/add-company
company-tag|GET|id|/api/\<lang>\/company-tag|curl -X GET http://127.0.0.1:5000/api/ko/company-tag?id=1



### api 설명
- company-name-candi: 회사이름 검색
- company-name-by-tag: 태그로 회사이름 검색
- add-company-tag: 회사에 tag 를 추가
- remove-company-tag: 특정 태그를 삭제
- add-company: 특정 회사를 추가
- company-tag: 저장된 태그를 보여준다.


## 전제조건

- db table 
    - 이름은 company 이다.
    - id 를 갖는다.
    - 회사 이름은 64자를 넘지 않는다.
- 회사이름은 "원하는 연속된 글자"가 들어가는 이름이 return 된다.
- 회사이름은 해당 locale 에 해당하는 company_name 만 검색된다.
- 태그추가시 |(delimiter) 는 입력이 안된다.
- `company-name-by-tag`
    - 검색태그는 한 번에 하나만 가능하다.
    - 태그는 정확히 일치할 때만 해당 회사이름이 반환된다.
    - 태그로 검색시, lang 이 en 이라면, company_name_en 값이 empty 이면, 아무것도 return 하지 않는다.
- `add-company-tag`
    - 태그 입력은 ',' 로 구분된다.
    - 태그 추가시 lang 이 en 이면, company_tag_en 에 값을 저장한다.
- `remove-company-tag`
    - 태그 삭제시 특정 회사에 대한 tag 를 삭제
- 태그정보추가, 태그정보삭제는 누구나 할 수 있다고 가정한다.
