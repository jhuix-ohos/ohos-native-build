export const tdCreate: () => number;

export const tdSend: (id: number, req: string) => void;

export const tdReceive: (timeout: number) => string | void;

export const tdExecute: (req: string) => string | void;

// Async

export const tdInit: (timeout: number) => void;

export const tdAsyncReceive: (callback: (response: string) => void) => void;

export const tdSetLogVerbosityLevel: (level: number) => void;

// Sync

export const tdJsonCreate: () => bigint;

export const tdJsonSend: (ptr: bigint, req: string) => void;

export const tdJsonReceive: (ptr: bigint, timeout: number) => string | void;

export const tdJsonExecute: (ptr: bigint, req: string) => string | void;

export const tdJsonDestroy: (ptr: bigint) => void;

// Async

export const tdClientCreate: (timeout: number) => bigint;

export const tdClientSend: (ptr: bigint, req: string) => void;

export const tdClientReceive: (ptr: bigint, callback: (response: string) => void) => void;

export const tdClientExecute: (ptr: bigint, req: string) => string | void;

export const tdClientDestroy: (ptr: bigint) => void;