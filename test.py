import pytest

from assembly.lang_5 import ContractRef

# we must explicitly publish this contract at the start of our scenario, and we refer to them
# via this contract ref type.
MY_CONTRACT = ContractRef('my_contract', '1.0.0', 5)


# tests are typically in classes, and we class-scope the network fixture. this makes granular reporting
# of long scenarios easy.
@pytest.mark.incremental
@pytest.mark.usefixtures('network', 'store')
class TestMyContract():

    aliases = ['alice']

    def test_reset(self, network):
        network.reset(txe_protocol=5, sympl_version=5)

    @pytest.mark.parametrize('alias', aliases)
    def test_register_identities(self, network, store, alias):
        store[alias] = network.register_key_alias()

    # after that we must publish our contract
    def test_publish(self, network, store):
        network.publish([MY_CONTRACT])

    # then we can make our two contract calls and check we see what we expect
    def test_my_first_function(self, network, store):
        result = network[
            store['alice']].my_contract["5-1.0.0"].my_api_function(n='120')
        assert result == 'wrote 120 to storage'

    def test_my_second_function(self, network, store):
        result = network[
            store['alice']].my_contract["5-1.0.0"].my_reader_function()
        assert result['value'] == '120'
