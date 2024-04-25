const { Sequelize, DataTypes} = require('sequelize')
// module.exports = new Sequelize({
const sequelize = new Sequelize({
    storage: 'db.sqlite',
    dialect: 'sqlite',
})

const User = sequelize.define(
    'User',
    {
        id: {
            type: DataTypes.INTEGER,
            allowNull: false,
            primaryKey: true,
            autoIncrement: true,
        },
        username: {
            type: DataTypes.STRING,
            defaultValue: 'None',
            allowNull: false,
        },
        firstName: {
            type: DataTypes.STRING,
            allowNull: false,
        },
        lastName: {
            type: DataTypes.STRING,
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
            allowNull: false,
            primaryKey: true,
            autoIncrement: true,
        },
        userId: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        text: {
            type: DataTypes.TEXT,
            defaultValue: 'None',
        },
        status: {
            type: DataTypes.TEXT,
        }
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
            allowNull: false,
            primaryKey: true,
            autoIncrement: true,
        },
        userId: {
            type: DataTypes.INTEGER,
            allowNull: false,
        },
        type: {
            type: DataTypes.TEXT,
        },

    },
    {
        timestamps: false,
    }
)

User.sync({ alter: true })
Logs.sync({ alter: true })
Devices.sync({ alter: true })
// Logs.sync()

module.exports = {'Users':User, 'Logs':Logs, 'Devices':Devices}