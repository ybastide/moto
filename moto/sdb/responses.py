from moto.core.responses import ActionResult, BaseResponse, EmptyResult

from .models import SimpleDBBackend, sdb_backends


class SimpleDBResponse(BaseResponse):
    def __init__(self) -> None:
        super().__init__(service_name="sdb")
        self.automated_parameter_parsing = True

    @property
    def sdb_backend(self) -> SimpleDBBackend:
        return sdb_backends[self.current_account][self.region]

    def create_domain(self) -> ActionResult:
        domain_name = self._get_param("DomainName")
        self.sdb_backend.create_domain(domain_name=domain_name)
        return EmptyResult()

    def delete_domain(self) -> ActionResult:
        domain_name = self._get_param("DomainName")
        self.sdb_backend.delete_domain(domain_name=domain_name)
        return EmptyResult()

    def list_domains(self) -> ActionResult:
        domain_names = self.sdb_backend.list_domains()
        result = {"DomainNames": domain_names}
        return ActionResult(result)

    def get_attributes(self) -> ActionResult:
        domain_name = self._get_param("DomainName")
        item_name = self._get_param("ItemName")
        attribute_names = self._get_param("AttributeNames")
        attributes = self.sdb_backend.get_attributes(
            domain_name=domain_name,
            item_name=item_name,
            attribute_names=attribute_names,
        )
        result = {"Attributes": attributes}
        return ActionResult(result)

    def put_attributes(self) -> str:
        domain_name = self._get_param("DomainName")
        item_name = self._get_param("ItemName")
        attributes = self._get_param("Attributes")
        self.sdb_backend.put_attributes(
            domain_name=domain_name, item_name=item_name, attributes=attributes
        )
        template = self.response_template(PUT_ATTRIBUTES_TEMPLATE)
        return template.render()

    def domain_metadata(self) -> str:
        domain_name = self._get_param("DomainName")
        metadata = self.sdb_backend.domain_metadata(domain_name=domain_name)
        template = self.response_template(DOMAIN_METADATA_TEMPLATE)
        return template.render(metadata=metadata)


CREATE_DOMAIN_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<CreateDomainResult  xmlns="http://sdb.amazonaws.com/doc/2009-04-15/"></CreateDomainResult>
"""


LIST_DOMAINS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<ListDomainsResponse  xmlns="http://sdb.amazonaws.com/doc/2009-04-15/">
    <ListDomainsResult>
        {% for name in domain_names %}
            <DomainName>{{ name }}</DomainName>
        {% endfor %}
        <NextToken>{{ next_token }}</NextToken>
    </ListDomainsResult>
</ListDomainsResponse>
"""

DELETE_DOMAIN_TEMPLATE = """<?xml version="1.0"?>
<DeleteDomainResponse xmlns="http://sdb.amazonaws.com/doc/2009-04-15/">
  <ResponseMetadata>
    <RequestId>64d9c3ac-ef19-2e3d-7a03-9ea46205eb71</RequestId>
    <BoxUsage>0.0055590278</BoxUsage>
  </ResponseMetadata>
</DeleteDomainResponse>"""

PUT_ATTRIBUTES_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<PutAttributesResult xmlns="http://sdb.amazonaws.com/doc/2009-04-15/"></PutAttributesResult>
"""

GET_ATTRIBUTES_TEMPLATE = """<GetAttributesResponse xmlns="http://sdb.amazonaws.com/doc/2009-04-15/">
  <ResponseMetadata>
    <RequestId>1549581b-12b7-11e3-895e-1334aEXAMPLE</RequestId>
  </ResponseMetadata>
  <GetAttributesResult>
{% for attribute in attributes %}
      <Attribute>
        <Name>{{ attribute["name"] }}</Name>
        <Value>{{ attribute["value"] }}</Value>
      </Attribute>
{% endfor %}
  </GetAttributesResult>
</GetAttributesResponse>"""


DOMAIN_METADATA_TEMPLATE = """<DomainMetadataResponse xmlns="http://sdb.amazonaws.com/doc/2009-04-15/">
  <DomainMetadataResult>
    <ItemCount>{{ metadata.item_count }}</ItemCount>
    <ItemNamesSizeBytes>{{ metadata.item_names_size_bytes }}</ItemNamesSizeBytes>
    <AttributeNameCount >{{ metadata.attribute_name_count }}</AttributeNameCount >
    <AttributeNamesSizeBytes>{{ metadata.attribute_names_size_bytes }}</AttributeNamesSizeBytes>
    <AttributeValueCount>{{ metadata.attribute_value_count }}</AttributeValueCount>
    <AttributeValuesSizeBytes>{{ metadata.attribute_values_size_bytes }}</AttributeValuesSizeBytes>
    <Timestamp>1225486466</Timestamp>
  </DomainMetadataResult>
  <ResponseMetadata>
    <RequestId>b1e8f1f7-42e9-494c-ad09-2674e557526d</RequestId>
    <BoxUsage>0.0000219907</BoxUsage>
  </ResponseMetadata>
</DomainMetadataResponse>"""
