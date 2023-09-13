from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import config as cfg
DB_URL = f"sqlite://{cfg.sys_id}/network_state.db"
engine = create_engine(DB_URL, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()

def initialize_database(reset=False):
    """Initialize or reset the database based on the reset parameter."""
    if reset:
        # Drop all tables if they exist
        Base.metadata.drop_all(engine)
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    alias = Column(Integer, nullable=False)
    pubkey = Column(LargeBinary, nullable=False)
    nym = Column(String)

    def __repr__(self):
        return f"User(alias={self.alias}, pubkey={self.pubkey}, nym={self.nym})"

class Broadcast(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True)
    block_hash = Column(LargeBinary, nullable=False)
    block_index = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)

    alias = Column(Integer, nullable=False)
    parent_id = Column(Integer, ForeignKey("broadcasts.id"))
    message = Column(String, nullable=False)

    parent = relationship("Broadcast", remote_side=[id], backref="children")

    def __repr__(self):
        return f"Broadcast(id={self.id}, alias={self.alias}, epoch={self.timestamp} parent={self.parent_id}, message={self.message})"





def db_process_i_block(
    mint_aliases, mint_pubkeys, update_aliases, update_pubkeys, nym_aliases, nym_nyms
):
    session = Session()

    try:
        for alias, pubkey in zip(mint_aliases, mint_pubkeys):
            user = User(alias=int.from_bytes(alias, "big"), pubkey=bytes(pubkey))
            session.add(user)

        for alias, pubkey in zip(update_aliases, update_pubkeys):
            user = (
                session.query(User)
                .filter_by(alias=int.from_bytes(alias, "big"))
                .first()
            )
            user.pubkey = bytes(pubkey)  # type: ignore

        for alias, nym in zip(nym_aliases, nym_nyms):
            user = (
                session.query(User)
                .filter_by(alias=int.from_bytes(alias, "big"))
                .first()
            )
            user.nym = nym.decode("utf-8")  # type: ignore

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def db_process_s_block(
    processed_broadcasts, processed_replies, block_hash, block_index, timestamp
):
    session = Session()

    try:
        for alias, _, message in processed_broadcasts:
            broadcast = Broadcast(
                block_hash=bytes(block_hash),
                block_index=int(block_index),
                timestamp=int.from_bytes(timestamp, "big"),
                alias=int.from_bytes(alias, "big"),
                message=message.decode("utf-8"),
            )
            session.add(broadcast)
            print("adding broadcast", broadcast)

        for alias, parent, message in processed_replies:
            parent_alias = int.from_bytes(parent.alias, "big")
            parent_epoch = parent.epoch
            print("~~~~~~")
            print("alias", parent_alias, type(parent_alias))
            print("epoch", parent_epoch, type(parent_epoch))
            print("~~~~~~")
            parent_broadcast = (
                session.query(Broadcast)
                .filter_by(alias=parent_alias, timestamp=parent_epoch)
                .first()
            )
            if parent_broadcast:
                parent_db_id = parent_broadcast.id
                print("found parent broadcast", parent_broadcast)
            else:
                raise ValueError(
                    f"Couldn't find parent broadcast for alias {parent.alias} and epoch {parent.epoch}"
                )
            broadcast = Broadcast(
                block_hash=bytes(block_hash),
                block_index=int(block_index),
                timestamp=int.from_bytes(timestamp, "big"),
                alias=int.from_bytes(alias, "big"),
                parent_id=parent_db_id,
                message=message.decode("utf-8"),
            )
            session.add(broadcast)
            print("adding reply", broadcast)
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def db_revert_i_block(
    unminted_aliases,
    reverted_update_aliases,
    reverted_update_pubkeys,
    reverted_nym_aliases,
    reverted_nym_nyms,
):
    session = Session()
    try:
        for alias in unminted_aliases:
            session.query(User).filter_by(alias=int.from_bytes(alias, "big")).delete()

        for alias, pubkey in zip(reverted_update_aliases, reverted_update_pubkeys):
            user = (
                session.query(User)
                .filter_by(alias=int.from_bytes(alias, "big"))
                .first()
            )
            user.pubkey = bytes(pubkey)  # type: ignore

        for alias, nym in zip(reverted_nym_aliases, reverted_nym_nyms):
            user = (
                session.query(User)
                .filter_by(alias=int.from_bytes(alias, "big"))
                .first()
            )
            user.nym = nym.decode("utf-8")  # type: ignore

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def db_revert_s_block(block_hash):
    session = Session()
    try:
        session.query(Broadcast).filter_by(block_hash=bytes(block_hash)).delete()
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def display_all_tables():
    """Display the contents of all tables in the database."""
    session = Session()

    # Loop through each table managed by Base's metadata
    print("********** DATABASE CONTENTS **********")
    for table in Base.metadata.sorted_tables:
        print(f"---- {table.name} ----")
        
        # Fetch all records from the current table
        for record in session.query(table).all():
            print(record)

        print("\n")  # Newline for separation
    print("***************************************")
    session.close()
