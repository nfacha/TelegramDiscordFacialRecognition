from discord import Role


def isStaff(author):
    canRun = False
    for role in author.roles:
        assert isinstance(role, Role)
        if role.id == "412667468960497670":  # Network Admin
            canRun = True
            break
        if role.id == "415216392225161217":  # Platform Admin
            canRun = True
            break
        if role.id == "366364594069045258":  # Support Staff
            canRun = True
            break
        if role.id == "354272516472176650":  # ResPT Dev
            canRun = True
            break
    return canRun