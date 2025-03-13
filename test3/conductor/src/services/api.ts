import axios from "axios";

export const api = axios.create({
  baseURL: "https://api.alicino.com.br/",
  //baseURL: "http://192.168.15.87:9530/",
})

