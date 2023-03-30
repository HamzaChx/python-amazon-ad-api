from ad_api.base import Client, sp_endpoint, fill_query_params, ApiResponse, Utils


class TargetsV3(Client):

    @sp_endpoint('/sp/targets/list', method='POST')
    def list_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:

        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), params=kwargs, headers=headers)

    @sp_endpoint('/sp/targets', method='POST')
    def create_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:

        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/targets', method='PUT')
    def edit_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:

        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

    @sp_endpoint('/sp/targets/delete', method='POST')
    def delete_product_targets(self, version: int = 3, **kwargs) -> ApiResponse:

        json_version = 'application/vnd.spTargetingClause.v' + str(version) + "+json"
        headers = {
            "Accept": json_version,
            "Content-Type": json_version
        }

        return self._request(kwargs.pop('path'), data=Utils.convert_body(kwargs.pop('body'), False), params=kwargs,
                             headers=headers)

