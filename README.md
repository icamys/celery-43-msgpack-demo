A repo for msgpack bug reproduction on Celery 4.3

Bug reproduction steps:

1. Create venv and install deps:
    ```bash
    $ python3 -m venv venv \
        && source venv/bin/activate \
        && pip install -r requirements.txt
    ```

2. Start the broker

    ```bash
    $ ./start_broker.sh
    ```

3. Start the worker

    ```bash
   ./start_worker.sh
    ```

4. Now you should get a decode message like this:

    ```bash
   [2019-10-01 13:33:12,077: CRITICAL/MainProcess] Can't decode message body: DecodeError(ExtraData([[], {}, ...
   ```

5. Comment out `task_serializer` and `accept_content` variables from [config.py](./config.py) so the contents
of the config file will look like this:

    ```python
    # task_serializer = 'msgpack'
    # accept_content = ['msgpack', 'application/x-msgpack']
    ```

6. The worker will automatically restart and you'll see such logs:

    ```bash
     -------------- celery@office-1 v4.3.0 (rhubarb)
    ---- **** ----- 
    --- * ***  * -- Linux-5.0.0-29-generic-x86_64-with-Ubuntu-18.04-bionic 2019-10-01 13:37:05
    -- * - **** --- 
    - ** ---------- [config]
    - ** ---------- .> app:         tasks:0x7fca61387d68
    - ** ---------- .> transport:   amqp://guest:**@localhost:5672//
    - ** ---------- .> results:     disabled://
    - *** --- * --- .> concurrency: 8 (prefork)
    -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    --- ***** ----- 
     -------------- [queues]
                    .> celery           exchange=celery(direct) key=celery
                    
    
    [tasks]
      . ns:create_list
      . ns:print_list_with_number
    
    [2019-10-01 13:37:05,625: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
    [2019-10-01 13:37:05,638: INFO/MainProcess] mingle: searching for neighbors
    [2019-10-01 13:37:06,669: INFO/MainProcess] mingle: all alone
    [2019-10-01 13:37:06,700: INFO/MainProcess] celery@office-1 ready.
    [2019-10-01 13:37:06,701: INFO/MainProcess] Received task: ns:create_list[987a2638-c9fe-43d3-826c-d87f321b463f]  
    [2019-10-01 13:37:06,845: INFO/MainProcess] Received task: ns:print_list_with_number[bc5eddec-1263-4551-bdbb-050667eefc82]  
    [2019-10-01 13:37:06,846: INFO/ForkPoolWorker-8] Task ns:create_list[987a2638-c9fe-43d3-826c-d87f321b463f] succeeded in 0.03962553100063815s: ['google.com']
    [2019-10-01 13:37:06,846: INFO/MainProcess] Received task: ns:print_list_with_number[6c0d7a3c-bbff-4ecb-8d68-ee2a576f1086]  
    [2019-10-01 13:37:06,846: INFO/ForkPoolWorker-2] ['google.com'] 1
    [2019-10-01 13:37:06,848: INFO/ForkPoolWorker-4] ['google.com'] 2
    [2019-10-01 13:37:06,865: INFO/ForkPoolWorker-2] Task ns:print_list_with_number[bc5eddec-1263-4551-bdbb-050667eefc82] succeeded in 0.01884706000055303s: ['google.com']
    [2019-10-01 13:37:06,866: INFO/MainProcess] Received task: ns:print_list_with_number[74969f15-6306-40d4-9e55-1cef594354d5]  
    [2019-10-01 13:37:06,867: INFO/ForkPoolWorker-6] ['google.com'] 2
    [2019-10-01 13:37:06,867: INFO/ForkPoolWorker-6] Task ns:print_list_with_number[74969f15-6306-40d4-9e55-1cef594354d5] succeeded in 0.0006498500006273389s: ['google.com']
    [2019-10-01 13:37:06,869: INFO/ForkPoolWorker-4] Task ns:print_list_with_number[6c0d7a3c-bbff-4ecb-8d68-ee2a576f1086] succeeded in 0.021286719998897752s: ['google.com']
    [2019-10-01 13:37:06,869: INFO/MainProcess] Received task: ns:print_list_with_number[04147cd4-1b2a-4143-98f8-02749dbbaa2b]  
    [2019-10-01 13:37:06,870: INFO/ForkPoolWorker-8] ['google.com'] 3
    [2019-10-01 13:37:06,870: INFO/ForkPoolWorker-8] Task ns:print_list_with_number[04147cd4-1b2a-4143-98f8-02749dbbaa2b] succeeded in 0.00020611299987649545s: ['google.com']
   ```

6.  Cleanup: remove the broker container:

    ```bash
   $ ./stop_rm_broker.sh 
   ```
