import logging
import asyncio
import orm
import hashlib
from models import User, Blog, Comment, next_id

from apis import APIError

logging.basicConfig(level=logging.INFO)

async def register_admin():
    email = 'yc@yc.com' 
    name = 'yc'
    passwd = '123456'
    '''
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    '''
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    #sha1_passwd = uid.encode('utf-8')+b':'+passwd.encode('utf-8')
    #passwd: this.passwd==='' ? '' : CryptoJS.SHA1(email + ':' + this.passwd).toString()
    s1 = '%s:%s' % (email, passwd)
    s2 = hashlib.sha1(s1.encode('utf-8')).hexdigest()
    sha1_passwd = uid.encode('utf-8')+b':'+s2.encode('utf-8')
    logging.info('uid:%s passwd:%s s2:%s' % (uid, passwd, s2))
    logging.info('pwd:%s sha1:%s' % (sha1_passwd, hashlib.sha1(sha1_passwd).hexdigest()))
    #sha1_passwd = '%s:%s' % (uid, passwd)
    #user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd).hexdigest(), image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    user.admin = True
    logging.info('开始添加管理员...')
    await user.save()
    logging.info('添加管理员完成...')

async def test(loop):
    await orm.create_pool(loop, user='www-data', password='yc1234', db='awesome')
    logging.info('开始调用User...')
    #u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    #logging.info('User调用结束...\n等待调用u.save...')
    #await u.save()
    #logging.info('调用u.save结束')
    await register_admin()
    logging.info('test调用结束...')


#要运行协程，需要使用事件循环
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    print('Test finished.')
    loop.close()



