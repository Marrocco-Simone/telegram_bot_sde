import {
  CoreACSearchResponse,
  GetUpdatesResponse,
  HuggingFaceResponse,
  Update,
  UpdateInfo,
} from "./types";
import fetch from "node-fetch";
import { config } from "dotenv";
import { parse } from "path";
config({ path: __dirname + "/./../../.env" });

// retrieve tokens from .env file
const BOT_TOKEN = process.env.BOT_TOKEN;
const CORE_AC_TOKEN = process.env.CORE_AC_TOKEN;
const HUGGING_FACE_TOKEN = process.env.HUGGING_FACE_TOKEN;

// urls
const telegram_url = `https://api.telegram.org/bot${BOT_TOKEN}`;
const core_ac_url = "https://api.core.ac.uk/v3/search/works/";
const huggin_face_url =
  "https://api-inference.huggingface.co/models/google/bigbird-pegasus-large-pubmed";

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function parseUpdate(update: Update) {
  const chat_id = update.message.chat.id.toString();
  const sender = update.message.chat.username;
  const message = update.message.text;

  console.log(`\n${sender} says ${message}`);

  const update_info: UpdateInfo = {
    chat_id,
    sender,
    message,
  };
  return update_info;
}

async function startServerPolling(
  parse_response: (update_info: UpdateInfo) => void
) {
  console.log("Server online. Waiting...");
  // id of the last parsed message
  let last_update = 0;
  while (true) {
    const r = await fetch(`${telegram_url}/getUpdates?offset=${last_update}`);
    const response: GetUpdatesResponse = await r.json();

    if (response.result.length > 0) {
      for (const update of response.result) {
        const update_info = parseUpdate(update);
        parse_response(update_info);
        last_update = update.update_id + 1;
      }
    }
    await sleep(1000);
  }
}

async function getResearchPapers(
  update_info: UpdateInfo,
  CORE_AC_TOKEN: string
) {
  const limit = 5;
  const r = await fetch(
    `${core_ac_url}?q=${update_info.message}&limit=${limit}`,
    {
      headers: { Authorization: `Bearer ${CORE_AC_TOKEN}` },
    }
  );
  const core_ac_response: CoreACSearchResponse = await r.json();
  return core_ac_response;
}

async function sendTelegramMessage(chat_id: string, return_msg: string) {
  await fetch(`${telegram_url}/sendMessage`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      chat_id: chat_id,
      text: return_msg,
    }),
  });
}

async function parse_response(update_info: UpdateInfo) {
  console.time('process request');

  const core_ac_response = await getResearchPapers(update_info, CORE_AC_TOKEN);
  let abstracts_text = "";
  try {
    for (const s of core_ac_response.results) {
      abstracts_text += `${s.abstract}\n`;
    }
  } catch (e) {
    const error_msg: string = core_ac_response["message"];
    console.log(`crashed core ac api. Reason: ${error_msg}`);
    const return_msg = `Sorry, request failed at CoreAc API. Reason: ${error_msg}. Retry`;
    await sendTelegramMessage(update_info.chat_id, return_msg);
    return;
  }

  console.log(
    `CoreAc responded with ${core_ac_response.results.length} results, out of ${core_ac_response.totalHits}`
  );
  console.log(`lenght of the abstract composition: ${abstracts_text.length}`);

  const hugging_face_response = await fetch(huggin_face_url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${HUGGING_FACE_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: abstracts_text,
  });
  const hugging_face_obj: HuggingFaceResponse =
    await hugging_face_response.json();
  console.log("HuggingFace responded");

  try {
    const return_msg = hugging_face_obj[0].summary_text;
    await sendTelegramMessage(update_info.chat_id, return_msg);
  } catch (e) {
    const error_msg: string = hugging_face_obj["error"];
    console.log(`crashed hugging face api. Reason: ${error_msg}`);
    const return_msg = `Sorry, request failed at HuggingFace API. Reason: ${error_msg}. Retry`;
    await sendTelegramMessage(update_info.chat_id, return_msg);
    return;
  }

  console.timeEnd('process request');
}

startServerPolling(parse_response);
