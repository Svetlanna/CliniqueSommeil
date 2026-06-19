const fs = require("fs");
const path = require("path");
const sqlite3 = require("sqlite3");

const cheminDB = path.join(__dirname, "clinique.db");
const cheminSchema = path.join(__dirname, "clinique.sql");

const schema = fs.readFileSync(cheminSchema, "utf8");
const db = new sqlite3.Database(cheminDB);

db.serialize(() => {
  db.exec(schema, (err) => {
    if (err) {
      console.error("Erreur lors de la création de la base :", err.message);
      process.exit(1);
    }
    console.log("Base de données créée et peuplée avec succès.");
    db.close();
  });
});
