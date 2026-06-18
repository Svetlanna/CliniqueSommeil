const express = require("express");
const app = express();
app.use(express.json());

app.use("/extract",   require("./routes/extract"));
app.use("/transform", require("./routes/transform"));
app.use("/load",      require("./routes/load"));

app.listen(3000, () => console.log("Serveur démarré sur le port 3000"));
