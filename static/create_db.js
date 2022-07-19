const Sequelize = require('sequelize')



const sequelize = new Sequelize("APIS", "root", "passer", {
    dialect: "mysql",
    host: "localhost"
});
   
try {
    sequelize.authenticate();
    console.log('Connecté à la base de données MySQL!');
    sequelize.query("SELECT *FROM users").then(([results, metadata]) => {
        console.log(results);
    })
} catch (error) {
    console.error('Impossible de se connecter, erreur suivante :', error);
}