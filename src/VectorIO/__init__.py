import numpy as np
from ovito.data import DataCollection, DataObject, Vectors
from ovito.io import FileReaderInterface, FileWriterInterface
from ovito.pipeline import Pipeline


class VectorFileWriter(FileWriterInterface):

    def exportable_type(self):
        return Vectors

    def supports_trajectories(self):
        return False

    def write(
        self,
        *,
        filename: str,
        frame: int,
        pipeline: Pipeline,
        object_ref: DataObject.Ref,
        **kwargs,
    ):
        data = pipeline.compute(frame)
        vectors = data.get(object_ref)

        vector_data = {}

        # Version
        vector_data["VectorFileWriter"] = 1.0

        # Meta data
        vector_data["Identifier"] = vectors.identifier
        vector_data["Title"] = vectors.title

        # All vector data
        for key in vectors.keys():
            vector_data[f"properties/{key}"] = vectors[key]

        # Export
        if filename.endswith(".csv"):
            export_data = []
            export_keys = []
            for key in vector_data:
                if key.startswith("properties"):
                    if vector_data[key].ndim == 1:
                        export_data.append(vector_data[key][:, np.newaxis])
                        export_keys.append(key.split("/")[1])
                    else:
                        export_data.append(vector_data[key])
                        export_keys.extend(
                            [key.split("/")[1]] * vector_data[key].shape[1]
                        )
            np.savetxt(
                filename,
                np.hstack(export_data),
                delimiter=", ",
                header=", ".join(export_keys),
            )
        else:
            np.savez_compressed(filename, **vector_data)


class VectorFileReader(FileReaderInterface):
    @staticmethod
    def detect(filename: str):
        # Try reading the file and validate the "VectorFileWriter" key (could validate version as well)
        try:
            vector_data = np.load(filename)
            return "VectorFileWriter" in vector_data
        except OSError:
            return False

    def parse(self, data: DataCollection, filename: str, *args, **kwargs):
        # Open file
        vector_data = np.load(filename)

        # Validate mandatory keys
        if "properties/Position" not in vector_data:
            raise KeyError("'Position' missing in vector data")
        if "properties/Direction" not in vector_data:
            raise KeyError("'Direction' missing in vector data")

        # Create surface mesh
        vectors = data.vectors.create(
            identifier=str(vector_data["Identifier"]), title=str(vector_data["Title"])
        )

        # set vectors and their properties
        for key in vector_data:
            if key.startswith("properties"):
                if key.split("/")[1] == "Position":
                    vectors.create_property(key.split("/")[1], data=vector_data[key])
