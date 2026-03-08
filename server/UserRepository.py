from models import db, UserModel


class UserRepository:

    @staticmethod
    def create_user(username: str, team: str, folder_access: str) -> int:
        if folder_access.find(".*") == -1:
            return -1

        user = UserModel(
                    username=username,
                    team=team,
                    folder_access=folder_access
                )

        db.session.add(user)
        db.session.commit()

        return user.id

    @staticmethod
    def modify_user_access(_id: int, folder: str) -> UserModel:
        folder = folder.replace(" ", "")

        user = UserModel.query.get(_id)

        if user and folder.find(".*") != -1:
            if len(user.folder_access):
                folder = "," + folder
            user.folder_access += "|".join(folder.split(","))
            db.session.commit()

        return user

    @staticmethod
    def user_exists(username: str) -> str or None:
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user.folder_access
        return None

    @staticmethod
    def view_all_users() -> tuple[UserModel]:
        return (
            UserModel.query.order_by(UserModel.id.asc).limit(100)
        )

