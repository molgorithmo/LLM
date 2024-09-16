import chromadb
import uuid
from Util.util import Utils

class VectorClient:
    def __init__(self) -> None:
        self.collection_name = Utils().collection_name
        self.client = chromadb.PersistentClient('vectorstore')
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def insert_data_to_collection(self, df):
        '''
        Creates collection based on the passed dataframe

        :param df: DataFrame on which the collection will be created.
        :return: Collection
        '''
        if not self.collection.count():
            for _, row in df.iterrows():
                self.collection.add(
                    documents=row['Techstack'],
                    metadatas={
                        'links': row['Links']
                    },
                    ids=[str(uuid.uuid4())]
                )
            return self.collection
    
    def get_collection(self):
        return self.client.get_collection(self.collection_name)