import logging

from celery import chain, group, Task
from app import app


class CreateListTask(Task):
    name_plain = 'create_list'
    namespace = 'ns'

    @property
    def name(self):
        return self.namespace + ':' + self.name_plain

    def run(self, *args, **kwargs):
        return ['google.com']


class PrintListWithNumberTask(Task):
    name_plain = 'print_list_with_number'
    namespace = 'ns'

    @property
    def name(self):
        return self.namespace + ':' + self.name_plain

    def run(self, the_list, number):
        logging.info(str(the_list) + ' ' + str(number + 1))
        return the_list


app.tasks.register(CreateListTask())
app.tasks.register(PrintListWithNumberTask())

res = chain(
    CreateListTask().s(),
    group([PrintListWithNumberTask().s(i) | PrintListWithNumberTask().s(i + 1) for i in range(2)])
)()
