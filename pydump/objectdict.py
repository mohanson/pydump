import typing


class ObjectDict(dict):
    def __getattr__(self, name: str) -> typing.Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        self[name] = value
