MY_DATA = Schema('MY_DATA', {'value': {'type': int}})


@clientside
def my_api_function(n: int) -> None:

    with PostTxArgs(PUBLIC, []):
        my_tx_function(MY_DATA(value=n))

    cvm.job_start()


@executable
def my_tx_function(md: MY_DATA) -> None:

    cvm.storage.put(Identifier('my_value'), MY_DATA, md)
    # dummy = cvm.ctx()

    cvm.job_completed('wrote {} to storage'.format(md.value))


@clientside
def my_reader_function() -> Optional[MY_DATA]:
    return cvm.storage.get(PUBLIC, MY_DATA, Identifier('my_value'))
