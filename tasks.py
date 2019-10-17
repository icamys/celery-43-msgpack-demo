import logging

from celery import chain, group, Task
from app import app


class CreateListTask(Task):
    name = 'create_list'

    def run(self, *args, **kwargs):
        return ['google.com']


class PrintListWithNumberTask(Task):
    name = 'print_list_with_number'

    def run(self, the_list, number):
        logging.info(str(the_list) + ' ' + str(number + 1))
        return the_list


app.tasks.register(CreateListTask())
app.tasks.register(PrintListWithNumberTask())

res = chain(
    CreateListTask().s(),
    group([PrintListWithNumberTask().s(i) | PrintListWithNumberTask().s(i + 1) for i in range(2)])
)()
