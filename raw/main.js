require("dotenv").config();
const WebSocket = require("ws");
const fs = require("fs");
const axios = require("axios");

const oAuth = process.env.OAUTH;
const CLIENT_ID = process.env.CLIENT_ID;
const ACCESS_TOKEN = process.env.ACCESS_TOKEN;
const nick = "Shakbot";

const socket = new WebSocket("wss://irc-ws.chat.twitch.tv:443");
const messagePath = "/data/messages.csv";
const dataPath = "/data/twitch.csv";

const channels = [
  "kyochandxd",
  "jazocorn",
  "shadowind_spl",
  "thatsrb2dude",
  "stormysenpai2",
  "jayy__sushi",
  "rdcgamingtwo",
  "rdcgamingthree",
  "rdcgamingfour",
  "rdcgamingfive",
  "rdcgaming",
];

const RDC_CHILDREN = [
  "rdcgamingtwo",
  "rdcgamingthree",
  "rdcgamingfour",
  "rdcgamingfive",
];

let liveRDC = false;

let start = false;
const checkLiveInterval = 60 * 5000;

async function checkRDCLiveStatus() {
  try {
    const userLogins = RDC_CHILDREN.map((u) => `user_login=${u}`).join("&");
    const url = `https://api.twitch.tv/helix/streams?${userLogins}`;
    const res = await axios.get(url, {
      headers: {
        "Client-ID": CLIENT_ID,
        Authorization: `Bearer ${ACCESS_TOKEN}`,
      },
    });
    liveRDC = res.data.data.length > 0;
    console.log(`[RDC] Live check: ${liveRDC ? "Live" : "Offline"}`);
  } catch (err) {
    console.error("[RDC] Live check error:", err.response?.data || err.message);
  }
}

setInterval(checkRDCLiveStatus, checkLiveInterval);
checkRDCLiveStatus();

const getChat = (raw) => {
  for (let i = 0; i < channels.length; i++) {
    if (raw.includes(`PRIVMSG #${channels[i]}`)) return channels[i];
  }
};

const getUser = (raw) => {
  if (!raw) return "";
  end = raw.indexOf("!");
  return raw.slice(1, end);
};

const filterMsg = (msg) => {
  if (!msg) return ""; // If invalid message return
  if (/[a-zA-Z0-9]+\.[a-zA-Z0-9]/.test(msg)) return ""; // Ignore messages that contains links / attempted links
  if (msg[0] == "!") return "";
  msg = msg.replace(/@[a-zA-Z0-9_]+/g, ""); // Remove any 'pings' in chat
  msg = msg.replace(/[^a-zA-Z\s]/g, ""); // Remove non alphabet or whitespace characters
  msg = msg.replace("  ", " "); // Remove double spaces
  return msg;
};

socket.addEventListener("open", () => {
  socket.send(`PASS oauth:${oAuth}`);
  socket.send(`NICK ${nick}`);
  for (let i = 0; i < channels.length; i++) {
    socket.send(`JOIN #${channels[i]}`);
  }
  if (!fs.existsSync(messagePath))
    fs.writeFileSync(messagePath, "username,message,channel,date\n", "utf-8");
  if (!fs.existsSync(dataPath))
    fs.writeFileSync(dataPath, "string,chat\n", "utf-8");
});

socket.addEventListener("message", (event) => {
  if (event.data.includes("PING")) socket.send("PONG");

  let raw = event.data;

  if (raw.includes("#rdcgaming :End of /NAMES list")) {
    start = true;
    return;
  }
  if (!start) return;

  if (raw.slice(1, 9) == "nightbot") return;
  if (raw.slice(1, 15) == "streamelements") return;
  if (raw.slice(1, 7) == "moobot") return;
  const chat = getChat(raw);
  const username = getUser(raw);
  raw = raw.split(":")[2];
  const msg = filterMsg(raw);
  const date = new Date();
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  if (
    username &&
    msg &&
    (chat != "rdcgaming" || (chat == "rdcgaming" && liveRDC))
  ) {
    console.log(`${date} | ${username}: ${msg.slice(0, -2)}`);
    fs.appendFileSync(
      messagePath,
      `${username},${msg.slice(0, -2)},${chat},${day}-${month}-${year}\n`,
      "utf-8"
    );
    console.log("Successfully written message to file.");
  }
});
