import logging
import asyncio
import orm
from models import User, Blog, Comment

logging.basicConfig(level=logging.INFO)

async def test(loop):
    await orm.create_pool(loop, user='www-data', password='yc1234', database='awesome')
    logging.info('开始调用User...')
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
    logging.info('User调用结束...\n等待调用u.save...')
    await u.save()
    logging.info('调用u.save结束')

#要运行协程，需要使用事件循环
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    print('Test finished.')
    loop.close()



