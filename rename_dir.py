import os

dir  =  [
        {
            "id": 57123,
            "text": "Unit1 测试A卷 应知应会",
            "index": 0,
            "parent_id": 0,
            "rank": 0,
            "start_page": 1,
            "book_id": 480
        },
        {
            "id": 57124,
            "text": "Unit1 测试B卷 扩展迁移",
            "index": 1,
            "parent_id": 0,
            "rank": 0,
            "start_page": 3,
            "book_id": 480
        },
        {
            "id": 57125,
            "text": "Unit2 测试A卷 应知应会",
            "index": 2,
            "parent_id": 0,
            "rank": 0,
            "start_page": 5,
            "book_id": 480
        },
        {
            "id": 57126,
            "text": "Unit2 测试B卷 扩展迁移",
            "index": 3,
            "parent_id": 0,
            "rank": 0,
            "start_page": 7,
            "book_id": 480
        },
        {
            "id": 57127,
            "text": "第一、二单元阶段测试卷",
            "index": 4,
            "parent_id": 0,
            "rank": 0,
            "start_page": 9,
            "book_id": 480
        },
        {
            "id": 57128,
            "text": "Unit3 测试A卷 应知应会",
            "index": 5,
            "parent_id": 0,
            "rank": 0,
            "start_page": 11,
            "book_id": 480
        },
        {
            "id": 57129,
            "text": "Unit3 测试B卷 扩展迁移",
            "index": 6,
            "parent_id": 0,
            "rank": 0,
            "start_page": 13,
            "book_id": 480
        },
        {
            "id": 57130,
            "text": "Unit4 测试A卷 应知应会",
            "index": 7,
            "parent_id": 0,
            "rank": 0,
            "start_page": 15,
            "book_id": 480
        },
        {
            "id": 57131,
            "text": "Unit4 测试B卷 扩展迁移",
            "index": 8,
            "parent_id": 0,
            "rank": 0,
            "start_page": 17,
            "book_id": 480
        },
        {
            "id": 57132,
            "text": "第三、四单元阶段测试卷",
            "index": 9,
            "parent_id": 0,
            "rank": 0,
            "start_page": 19,
            "book_id": 480
        },
        {
            "id": 57133,
            "text": "期中测试A卷",
            "index": 10,
            "parent_id": 0,
            "rank": 0,
            "start_page": 21,
            "book_id": 480
        },
        {
            "id": 57134,
            "text": "期中测试B卷",
            "index": 11,
            "parent_id": 0,
            "rank": 0,
            "start_page": 23,
            "book_id": 480
        },
        {
            "id": 57135,
            "text": "Unit5 测试A卷 应知应会",
            "index": 12,
            "parent_id": 0,
            "rank": 0,
            "start_page": 25,
            "book_id": 480
        },
        {
            "id": 57136,
            "text": "Unit5 测试B卷 扩展迁移",
            "index": 13,
            "parent_id": 0,
            "rank": 0,
            "start_page": 27,
            "book_id": 480
        },
        {
            "id": 57137,
            "text": "Unit6 测试A卷 应知应会",
            "index": 14,
            "parent_id": 0,
            "rank": 0,
            "start_page": 29,
            "book_id": 480
        },
        {
            "id": 57138,
            "text": "Unit6 测试B卷 扩展迁移",
            "index": 15,
            "parent_id": 0,
            "rank": 0,
            "start_page": 31,
            "book_id": 480
        },
        {
            "id": 57139,
            "text": "第五、六单元阶段测试卷",
            "index": 16,
            "parent_id": 0,
            "rank": 0,
            "start_page": 33,
            "book_id": 480
        },
        {
            "id": 57140,
            "text": "Unit7 测试A卷 应知应会",
            "index": 17,
            "parent_id": 0,
            "rank": 0,
            "start_page": 35,
            "book_id": 480
        },
        {
            "id": 57141,
            "text": "Unit7 测试B卷 扩展迁移",
            "index": 18,
            "parent_id": 0,
            "rank": 0,
            "start_page": 37,
            "book_id": 480
        },
        {
            "id": 57142,
            "text": "Unit8 测试A卷 应知应会",
            "index": 19,
            "parent_id": 0,
            "rank": 0,
            "start_page": 39,
            "book_id": 480
        },
        {
            "id": 57143,
            "text": "Unit8 测试B卷 扩展迁移",
            "index": 20,
            "parent_id": 0,
            "rank": 0,
            "start_page": 41,
            "book_id": 480
        },
        {
            "id": 57144,
            "text": "第七、八单元阶段测试卷",
            "index": 21,
            "parent_id": 0,
            "rank": 0,
            "start_page": 43,
            "book_id": 480
        },
        {
            "id": 57145,
            "text": "分类复习练习A卷(词汇)",
            "index": 22,
            "parent_id": 0,
            "rank": 0,
            "start_page": 45,
            "book_id": 480
        },
        {
            "id": 57146,
            "text": "分类复习练习B卷(日常交际用语)",
            "index": 23,
            "parent_id": 0,
            "rank": 0,
            "start_page": 47,
            "book_id": 480
        },
        {
            "id": 57147,
            "text": "分类复习练习C卷(阅读理解)",
            "index": 24,
            "parent_id": 0,
            "rank": 0,
            "start_page": 49,
            "book_id": 480
        },
        {
            "id": 57148,
            "text": "分类复习练习D卷(作文)",
            "index": 25,
            "parent_id": 0,
            "rank": 0,
            "start_page": 51,
            "book_id": 480
        },
        {
            "id": 57149,
            "text": "期末测试A卷",
            "index": 26,
            "parent_id": 0,
            "rank": 0,
            "start_page": 53,
            "book_id": 480
        },
        {
            "id": 57150,
            "text": "期末测试B卷",
            "index": 27,
            "parent_id": 0,
            "rank": 0,
            "start_page": 55,
            "book_id": 480
        },
        {
            "id": 57151,
            "text": "期末测试C卷",
            "index": 28,
            "parent_id": 0,
            "rank": 0,
            "start_page": 57,
            "book_id": 480
        },
        {
            "id": 57152,
            "text": "期末测试D卷",
            "index": 29,
            "parent_id": 0,
            "rank": 0,
            "start_page": 59,
            "book_id": 480
        }
    ]

start_page = []
id = []
text = []
for search_text in dir:
    text.append(search_text['text'])

i = -1
for dic in dir:
    i += 1

   ##khjk\\\12 if  '测试' in text[i] :
    #    start_page.append(dic['start_page'])
    #    id.append(dic['id'])
    #if  '培优' in text[i] :
    #    start_page.append(dic['start_page'])
    #    id.append(dic['id'])
    #if '综合'  in text[i]:
    #    start_page.append(dic['start_page'])
    #    id.append(dic['id'])

    start_page.append(dic['start_page'])
    id.append(dic['id'])


dict(zip(start_page,id))
new_id = dict(zip(start_page,id)).values()

root = os.getcwd()
bookid = str(dir[0]['book_id'])
# bookid = input('input file name: ')
# bookid = str(143)
file_path = root + '/' + bookid + '/'

name = list(new_id)
name.sort()
page = sorted(os.listdir(file_path), key=lambda b: int(b.split('.')[0]))
i = 0
for file in page:
    src = os.path.join(file_path, file)
    dst = os.path.join(file_path, str(name[i]) + '.png')
    os.rename(src, dst)
    print(str(name) + '.png')
    i+= 1