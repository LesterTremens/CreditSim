export async function simulateCredit(apiUrl, payload) {
    const res = await fetch(`${apiUrl}/simulate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  
    if (!res.ok) {
      const body = await res.json().catch(() => null);
      const msg =
        typeof body?.detail === "string"
          ? body.detail
          : `Request failed (${res.status})`;
      throw new Error(msg);
    }
  
    return await res.json();
  }