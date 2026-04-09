const amountPattern = /(-?[\d\s.,]+)/;

export function parseMoney(raw: string): { amount: number; currency?: string } {
  const cleaned = raw.trim().replace(/\u00A0/g, ' ');
  const match = cleaned.match(amountPattern);
  if (!match) {
    throw new Error(`Unable to parse money amount from: "${raw}"`);
  }

  const numericPortion = match[1].replace(/\s/g, '').replace(/\.(?=.*\.)/g, '').replace(',', '.');
  const amount = Number(numericPortion);
  if (Number.isNaN(amount)) {
    throw new Error(`Unable to normalize numeric amount from: "${raw}"`);
  }

  const currency = cleaned.replace(match[1], '').trim() || undefined;
  return { amount, currency };
}
