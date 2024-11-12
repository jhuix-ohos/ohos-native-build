export const tdCreate: () => number;

export const tdSend: (number, string) => void;

export const tdReceive: (double) => string | void;

export const tdExecute: (string) => string | void;

export const tdSetLogVerbosityLevel: (number) => void;

export const tdJsonCreate: () => bigint;

export const tdJsonSend: (bigint, string) => void;

export const tdJsonReceive: (bigint, double) => string | void;

export const tdJsonExecute: (bigint, string) => string | void;

export const tdJsonDestroy: (bigint) => void;