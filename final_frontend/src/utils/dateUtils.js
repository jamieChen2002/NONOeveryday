export function prevMonth(monthStr) {
  const date = new Date(monthStr + "-01");
  date.setMonth(date.getMonth() - 1);
  return date.toISOString().slice(0, 7);
}
