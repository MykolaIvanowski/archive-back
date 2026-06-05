from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app_user_tenancy.db.base import Base

### shared‑schema
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tenant_id = Column(String, Index=True, nullable=False)

    full_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    marketing_opt_in = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now)
    deleted = Column(Boolean, default=False)


### Different approach for tenants
### 0. shared schema (usually not used )
# users
# orders
# documents
### 1 Shared DB, Isolated Schemas
# tenant1.users
# tenant1.orders
# tenant2.users
# tenant2.orders
### 2. DB - per tenant
# db_tenant1 (users, orders, documents)
# db_tenant2 (users, orders, documents)
# db_tenant3 (users, orders, documents)
### 3. Hybrid
# shared.users
# shared.documents
#
# tenant1.custom_fields
# tenant1.workflows
# tenant2.custom_fields
# tenant2.workflows

