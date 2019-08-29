'''
hey,buddy!the following words are the introduction for the not good code, please do not mind.
    我写了一个类,这个类的名字叫做vehical.(表的名字也叫vehical)
    接下来我将从以下方面来介绍what the vehical can do for you:
    1.类的初始化：

        1.1#############################################################################################################
        创建到数据库的连接
        self.connection = pymysql.connect(host='127.0.0.2',
                                     user='root',
                                     password='0327',
                                     # db='xieyuanliang',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        然后根据参数自行修改

        1.2#############################################################################################################
        在数据库账户中默认创建了database:win
        在database：win中默认创建了table的名字为vehical

        1.3#############################################################################################################
        创建表vehical：vehical( car_id, color_attras, type_attras, Li_plate, video_detect_time, picture_path )括号中的为表的
        各个属性

    2.类的方法所实现的功能：

        ################################################################################################################
        2.1 插入数据：insert_data(self, data)
        data的输入数据格式如下所示：
        data = {'car_id': 1, 'color_attras': 1, 'type_attras': 1, 'Li_plate': '421',
            'video_detect_time': '2018-09-03 11:30:05', 'picture_path': '/home/xyl/桌面/1.jpg'}
        其中'car_id'和'picture_path'不可为空
        ################################################################################################################
        2.2 计算违规车辆的总数：
        使用方式为：
            a=vehical()#类的实例化
            a.number
            返回数据格式为：{'num': 3}
        ################################################################################################################
        2.3 实现筛选特定颜色的车
        类方法：select_which_color(self, color, field = True)
        输入参数： color为所需筛选的格式,这里采用数字来筛选
                 field为筛选的反条件，若field为True则筛选color颜色的车，若field为False则筛选不是color颜色的车
        输入参数的格式：color=(1,2,3),color为元组或者列表
        输出参数：因为此参数迭代生成，所以输出为：{'car_id': 1}
        调用方式：
                a = vehical()
                b = a.select_which_type_car([1,2,3])
                for i in b:
                    print(i)
        ################################################################################################################
        2.4 对车的出现时间进行筛选
        类方法：select_between_time(self, start, stop)
        输入参数：start：为视频开始的时间
                stop：为视频结束的时间
        输入参数的格式：start="2018-09-03 10:30:05", stop="2018-09-03 12:30:05"
        输出参数与2.3输出一样
        调用方式：
                a = vehical()
                b = a.select_between_time(start="2018-09-03 10:30:05", stop="2018-09-03 12:30:05")
                for i in b:
                    print(i)
        ################################################################################################################
        2.5 对车型进行筛选
        类方法：select_which_type_car(self, type_car, field=True)
        输入参数：type_car为所需筛选的格式,这里采用数字来筛选
                field为筛选的反条件，若field为True则筛选type_car类型的车，若field为False则筛选不是type_car类型的车
        输入参数的格式为：type_car = (1,2,3)
        输出与2.3输出一样
        调用方式：
                a=vehical()
                b = a.select_which_type_car([1])
                for i in b:
                    print(i)
        ################################################################################################################
        2.6 对车牌进行模糊筛选
        类方法：select_fuzzy_liplate(self, num_liplate)
        输入参数：num_liplate
        输入参数格式为：num_liplate = '666'
        输入与2.3输出一样
        调用方式：
                a=vehical()
                b = a.select_fuzzy_liplate('484')
                for i in b:
                    print(i)

    3.实现了一个查询类的方法的装饰器：
        函数名：Inquire_car(select_method)
        调用方式：即在所定义的类方法上加上@语法糖+装饰器函数，如下所示
                @Inquire_car
                def select_between_time(self, start, stop):
        迭代的单个输出：{'car_id': 1}
        加了@Inquire_car的迭代的单个输出：{'car_id': 1, 'color_attras': 1, 'type_attras': 1, 'Li_plate': '421', 'video_detect_time': '2018-09-03 11:30:05', 'picture_path': '/home/xyl/桌面/1.jpg'}
        实现此装饰器的目的：返回所查询结果的所有属性，而不是单个car_id的号码（装饰器可按需更改)

enmmmm,the introduction is boring, but detailed. Writed by xie yuanliang in 2019.6.22 16:35:00

'''



import pymysql.cursors


def Inquire_car(select_method):  # 装饰类的方法,查询车各个的属性，可以修改
    def wrapper(self, *args, **kwargs):
        with self.connection.cursor() as cursor:
            for i in select_method(self, *args, **kwargs):
                sql = ("select * from vehical where car_id = %d" % i['car_id'])
                cursor.execute(sql)
                result = cursor.fetchone()
                yield result
        self.connection.commit()

    return wrapper
#类
class vehical(object):
    def __init__(self):
        self.connection = pymysql.connect(host='127.0.0.2',
                                     user='root',
                                     password='0327',
                                     # db='xieyuanliang',
                                     charset='utf8mb4',  # 这里不太懂
                                     cursorclass=pymysql.cursors.DictCursor)  # 这里也不太懂
        self.init()


    def init(self):
        with self.connection.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS win;')
            cursor.execute('USE win')
        self.connection.commit()
        print('已连接到数据库')
        self.creat_tabel()
    @property
    def delete_table(self, table_name = 'vehical'):
        with self.connection.cursor() as cursor:
            cursor.execute('drop table if exists %s' % table_name)
        self.connection.commit()
        print('删除已存在的vehical表')


    def creat_tabel(self, database_name='win', table_name='vehical'):
        with self.connection.cursor() as cursor:
            #cursor.execute('drop table if exists %s'%table_name)#########!!!!!!!!!!!!!!!!!!测试语句,正式程序请注释此句！！！！！！！！！！！！！！！！！！！！！！！！！
            cursor.execute('USE %s' %database_name)
            self.delete_table
            cursor.execute('CREATE TABLE IF NOT EXISTS %s '
                           '('
                               'car_id  INT NOT NULL,'
                               'color_attras INT  NULL,'
                               'type_attras INT NULL,'
                               'Li_plate CHAR(20) NULL,'
                               'video_detect_time CHAR(30) NULL,'
                               'picture_path CHAR(100) NOT NULL,'
                               'PRIMARY KEY(car_id) '
                           ')ENGINE = InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1; '%table_name
                           )
        self.connection.commit()
        print('表初始化完毕')

    def insert_data(self, data):#此data为字典,format:{'car_id':6,'picture_path':~~}:
        with self.connection.cursor() as cursor:
            #"INSERT INTO `albums` (`ALBUM_ID`,ALBUM_NAME, `ARTIST_ID`) VALUES (%s, %s, %s)"
            sql = ("INSERT INTO vehical( car_id, color_attras, type_attras, Li_plate, video_detect_time, picture_path )"
                  "VALUES(%s, %s, %s, %s, %s, %s)")
                   #%data['color_attras'], %data['type_attras'], %data['Li_plate'], data['video_detect_time'], data['picture_path'])
            cursor.execute(sql, (data['car_id'], data['color_attras'], data['type_attras'], data['Li_plate'], data['video_detect_time'], data['picture_path']))
        self.connection.commit()
        print('插入数据成功')

    #计算违规车辆的总数
    @property
    def number(self):
        with self.connection.cursor() as cursor:
            sql = ("select count(car_id) as num from vehical;")
            cursor.execute(sql)
            number = cursor.fetchone()
        self.connection.commit()
        return number

    # #数据迭代器
    # def extract_data(self):
    #
    #     pass

    #对数据库进行筛选
    def generate_str(self, a):#a为列表或者元组
        b = '('
        for i in range(len(a)):

            if i == len(a) - 1:
                b += str(a[i])
                b += ')'
            else:
                b += str(a[i])
                b += ', '
        return b
    @Inquire_car
    def select_which_color(self, color, field = True):#此筛选颜色的模块已经实现迭代器生成,一次返回一个数据

        str = self.generate_str(color)

        with self.connection.cursor() as cursor:
            sql1 = ("select car_id from vehical where color_attras in %s ;"%str)
            sql2 = ("select car_id from vehical where color_attras not in %s;"%str)
            if field:
                cursor.execute(sql1)
            else:
                cursor.execute(sql2)
            while (True):
                car_id = cursor.fetchone()
            #self.connection.commit()
                if car_id is None:
                    break
                yield car_id#后面要把这个变成一个迭代器
        self.connection.commit()

    #对车的出现时间进行筛选
    @Inquire_car
    def select_between_time(self, start, stop):
        start ="'"+start+"'"
        stop  ="'"+stop +"'"
        with self.connection.cursor() as cursor:
            sql = ('select car_id from vehical where video_detect_time between %s and %s;' % (start, stop))
            cursor.execute(sql)
            while (True):
                car_id = cursor.fetchone()
                # self.connection.commit()
                if car_id is None:
                    break
                yield car_id  # 后面要把这个变成一个迭代器
        self.connection.commit()

    #对车型进行筛选
    @Inquire_car
    def select_which_type_car(self, type_car, field=True):#如果field为True则条件为正,否则条件为筛选不是这些车型的所有车辆
        str = self.generate_str(type_car)
        with self.connection.cursor() as cursor:
            sql1 = ("select car_id from vehical where type_attras in %s " % str)
            sql2 = ("select car_id from vehical where type_attras not in %s" % str)
            if field:
                cursor.execute(sql1)
            else:
                cursor.execute(sql2)
            while (True):
                car_id = cursor.fetchone()
                # self.connection.commit()
                if car_id is None:
                    break
                yield car_id  # 后面要把这个变成一个迭代器
        self.connection.commit()

    #对车牌进行模糊筛选
    def generrate_str_liplate(self, a):
        b = "'"
        a = b + '%' + a + '%' + b
        return a
    @Inquire_car
    def select_fuzzy_liplate(self, num_liplate):#num_liplate is str

        with self.connection.cursor() as cursor:
            str = self.generrate_str_liplate(num_liplate)
            sql = ("select car_id from vehical where Li_plate like %s"%str)
            cursor.execute(sql)
            while (True):
                car_id = cursor.fetchone()
                # self.connection.commit()
                if car_id is None:
                    break
                yield car_id  # 后面要把这个变成一个迭代器
        self.connection.commit()














if __name__ == '__main__':
    a = vehical()
    data = {'car_id': 1, 'color_attras': 1, 'type_attras': 1, 'Li_plate': '421',
            'video_detect_time': '2018-09-03 11:30:05', 'picture_path': '/home/xyl/桌面/1.jpg'}
    data1 = {'car_id': 2, 'color_attras': 2, 'type_attras': 1, 'Li_plate': '281484',
            'video_detect_time': '2018-09-03 11:30:06', 'picture_path': '/home/xyl/桌面/1.jpg'}
    data2 = {'car_id': 3, 'color_attras': 3, 'type_attras': 2, 'Li_plate': '777',
            'video_detect_time': '2018-09-03 11:30:05', 'picture_path': '/home/xyl/桌面/1.jpg'}
    #c=[]
    a.insert_data(data)
    a.insert_data(data1)
    a.insert_data(data2)
    #print('插入数据成功!')
    print(a.number)#统计违规车辆个数
    b = a.select_between_time(start="2018-09-03 10:30:05", stop="2018-09-03 12:30:05")#筛选时间
    print('时间筛选：')
    for i in b:
        print(i)
    b = a.select_which_type_car([1])
    print('车型筛选：')
    for i in b:
        print(i)
    b = a.select_which_color((1, 2, 3))#color已经用数字表示了，技术上的原因
    print('颜色筛选')
    for i in b:
        print(i)
    b = a.select_fuzzy_liplate('484')#输入字符串格式
    print('车牌筛选:')
    for i in b:
        print(i)
    print('以上都是+@Inquire_car装饰器返回的数据格式，每行为迭代器单个返回的格式')