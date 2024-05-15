const { Sequelize, DataTypes} = require('sequelize')
// module.exports = new Sequelize({
const sequelize = new Sequelize({
    storage: 'db.sqlite',
    dialect: 'sqlite',
})

const Users = sequelize.define(
    'Users',
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            allowNull: false,
        },
        email: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        password: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        logo: {
            type: DataTypes.STRING,
            defaultValue: '/static/userdata/avatar/logo.png',
        },
        name: {
            type: DataTypes.TEXT,
            allowNull: false,
        },
        surname: {
            type: DataTypes.TEXT,
        },
        role: {
            type: DataTypes.STRING,
            allowNull: false,
            defaultValue: 'user',
        },
    },
    {
        timestamps: false,
    }
)

const Sessions = sequelize.define(
    'Sessions',
    {
        id: {
            type: DataTypes.STRING,
            primaryKey: true,
            allowNull: false,
        },
        user_id: {
            type: DataTypes.INTEGER,
            allowNull: false,
        }
    },
    {timestamps: false}
)

const Questions = sequelize.define(
    'Questions',
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            allowNull: false,
        },
        user_id: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        question: {
            type: DataTypes.TEXT('tiny'),
            allowNull: false,
        },
        description: {
            type: DataTypes.TEXT,
        },
    },
    {
        updatedAt: false,
    }
)

const Devices = sequelize.define(
    'Devices',
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            allowNull: false,
        },
        user_id: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        logo: {
            type: DataTypes.STRING,
            defaultValue: '/static/images/devices_logo/logo.png',
        },
        title: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        room: {
            type: DataTypes.TEXT('tiny'),
            defaultValue: 'Main',
        },
        type: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        settings: {
            type: DataTypes.JSON,
            allowNull: false,
        },
    },
    {
        timestamps: false,
    }
)

const Scenarios = sequelize.define(
    'Scenarios',
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            allowNull: false,
        },
        title: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        description: {
            type: DataTypes.TEXT,
        },
        user_id: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        status: {
            type: DataTypes.BOOLEAN,
            allowNull: false,
        },
        commands: {
            type: DataTypes.JSON,
            allowNull: false,
        },
    },
    {
        timestamps: false,
    }
)

const Logs = sequelize.define(
    'Logs',
    {
        id: {
            type: DataTypes.INTEGER,
            primaryKey: true,
            autoIncrement: true,
            allowNull: false,
        },
        raspberry_id: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        text: {
            type: DataTypes.TEXT,
            allowNull: false,
        },
        type: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        error: {
            type: DataTypes.BOOLEAN,
            defaultValue: false,
        }
    },
    {
        updatedAt: false,
    }
)

Users.sync({ alter: true })
Devices.sync({ alter: true })
Questions.sync({ alter: true })
Scenarios.sync({ alter: true })
Sessions.sync({ alter: true })
Logs.sync({ alter: true })

module.exports = {'Users': Users, 'Devices': Devices, 'Questions': Questions, 'Scenarios': Scenarios, 'Sessions': Sessions, 'Logs': Logs}