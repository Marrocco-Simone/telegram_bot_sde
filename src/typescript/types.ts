export type UpdateInfo = {
  chat_id: string;
  sender: string;
  message: string;
}

export type User = {
  // unique id of the user
  id: number;
  // other data of the user
  is_bot: boolean;
  first_name: string;
  last_name: string;
  username: string;
  language_code: string; // en
};

export type Chat = {
  //  type of conversation: private, group, ...
  type: string;
  //  same fields as USER
  id: number;
  first_name: string;
  last_name: string;
  username: string;
};

export type Message = {
  //  id for the new message
  message_id: number;
  from: User;
  chat: Chat;
  //  unix date
  date: number;
  //  the text sent
  text: string;
};

export type Update = {
  //  id for the new update
  update_id: number;
  message: Message;
};

// the complete response object
export type GetUpdatesResponse = {
  ok: boolean;
  result: [Update];
};

export type SendMessageResponse = {
  ok: boolean;
  result: Message;
};

export type CoreACWork = {
  accepted_date: Date;
  authors: [string];
  contributors: [string];
  created_date: Date;
  data_provider: [string];
  deposited_date: Date;
  abstringact: string;
  document_type: string;
  doi: string;
  oai: string;
  download_url: string;
  full_text: string;
  id: number;
  identifiers: [any];
  title: string;
  language: any;
  published_date: Date;
  publisher: any;
  references: [any];
  source_fulltext_urls: [string];
  updated_date: Date;
  year_published: string;
  links: [string];
  tags: [string];
  fulltext_status: string;
  subjects: [string];
  deleted: string;
  journals: string;
  repositories: [any];
  repository_document: any;
  urls: [string];
  disabled: number;
  last_update: Date;
};

export type CoreACSearchResponse = {
  totalHits: number;
  limit: number;
  offset: number;
  scrollId: string;
  results: [CoreACWork];
  tooks: [string];
  esTook: number;
};

export type HuggingFaceResponse = [{ summary_text: string }];
