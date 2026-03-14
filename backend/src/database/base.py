from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from . import db
from .utils import utc_now


class CRUDMixin:
    __abstract__ = True

    def _set_attributes(self, **kwargs):
        for attr, value in kwargs.items():
            if hasattr(self, attr) or isinstance(
                getattr(type(self), attr, None), property
            ):
                setattr(self, attr, value)

        return self

    @classmethod
    def create(cls, commit: bool = True, **kwargs):
        obj = cls()._set_attributes(**kwargs)
        return obj.save(commit)

    def update(self, commit: bool = True, **kwargs):
        self._set_attributes(**kwargs)

        return self.save(commit)

    def save(self, commit: bool = True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit: bool = True):
        db.session.delete(self)
        if commit:
            db.session.commit()

    @classmethod
    def get_by_id(cls, model_id: int):
        obj = db.session.get(cls, model_id)

        return obj if obj and not obj.is_deleted else None


class BaseModel(CRUDMixin, db.Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=utc_now)
    modified_at: Mapped[datetime] = mapped_column(default=utc_now, onupdate=utc_now)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} id({self.id}) deleted({self.is_deleted})"
