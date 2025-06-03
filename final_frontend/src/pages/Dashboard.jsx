import React, { useState, useEffect, useRef } from "react";
import { prevMonth } from "../utils/dateUtils";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

const Dashboard = () => {
  const [data, setData] = useState({
    indicators: { income: { value: 0, pct: null }, cost: { value: 0, pct: null }, pest: { value: 0, pct: null } },
    total_cost: 0,
    total_income: 0,
    pest_count: 0,
    record_count: 0,
    pest_detail: [],
    category_detail: [],
    cost_detail: [],
    income_detail: [],
    cost_money_detail: [],
    daily_counts: [],
    daily_pest_counts: [],
    ai_summary: {},
    alerts: [],
    summary: ""
  });
  const [selectedMonth, setSelectedMonth] = useState("2025-06");
  const [pestAdvice, setPestAdvice] = useState([]);
  const pestAdviceCache = useRef({});

  const handlePrevMonth = () => {
    setSelectedMonth(prevMonth(selectedMonth));
  };

  const handleNextMonth = () => {
    const date = new Date(selectedMonth + "-01");
    date.setMonth(date.getMonth() + 1);
    setSelectedMonth(date.toISOString().slice(0, 7));
  };

  useEffect(() => {
    // 切換月份，先清空舊資料與建議
    setData({
      indicators: { income: { value: 0, pct: null }, cost: { value: 0, pct: null }, pest: { value: 0, pct: null } },
      total_cost: 0,
      total_income: 0,
      pest_count: 0,
      record_count: 0,
      pest_detail: [],
      category_detail: [],
      cost_detail: [],
      income_detail: [],
      cost_money_detail: [],
      daily_counts: [],
      daily_pest_counts: [],
      ai_summary: {},
      alerts: [],
      summary: ""
    });
    setPestAdvice([]);
    fetch(`/api/dashboard?month=${selectedMonth}`)
      .then((res) => {
        if (!res.ok) throw new Error("API 錯誤");
        return res.json();
      })
      .then((json) => {
        console.log(">>> data-from-indicators:", json);
        setData((prev) => ({
          ...prev,
          ...json
        }));
      })
      .catch((err) => {
        console.error("Dashboard 讀取失敗：", err);
        setData((prev) => ({
          ...prev,
          indicators: { income: { value: 0, pct: null }, cost: { value: 0, pct: null }, pest: { value: 0, pct: null } },
          total_cost: 0,
          total_income: 0,
          pest_count: 0,
          record_count: 0,
          pest_detail: [],
          category_detail: [],
          cost_detail: [],
          income_detail: [],
          cost_money_detail: [],
          daily_counts: [],
          daily_pest_counts: [],
          ai_summary: { [selectedMonth]: "無法取得摘要" },
          alerts: [],
          summary: ""
        }));
      });
  }, [selectedMonth]);


  const {
    indicators,
    total_cost,
    total_income,
    pest_count,
    record_count,
    pest_detail,
    category_detail,
    cost_detail,
    income_detail,
    cost_money_detail: costMoneyDetail,
    income_money_detail: incomeMoneyDetail,
    daily_counts,
    daily_pest_counts,
    ai_summary,
    alerts,
    summary
  } = data;

  useEffect(() => {
    console.log("▶ [DEBUG] selectedMonth =", selectedMonth);
    console.log("▶ [DEBUG] pest_detail =", pest_detail);
    
    // 當 pest_detail 更新時，先檢查快取
    if (!pest_detail || pest_detail.length === 0) {
      setPestAdvice([]);
      return;
    }
    // 快取鍵使用 selectedMonth
    if (pestAdviceCache.current[selectedMonth]) {
      setPestAdvice(pestAdviceCache.current[selectedMonth]);
      return;
    }
    const pests = pest_detail.map((item) => item.name).join(",");
    fetch(`/api/pest_advice?pests=${encodeURIComponent(pests)}`)
      .then((res) => res.json())
      .then((resp) => {
        const results = resp.results || [];
        // 將結果存入快取
        pestAdviceCache.current[selectedMonth] = results;
        setPestAdvice(results);
      })
      .catch(() => {
        setPestAdvice([]);
      });
  }, [pest_detail, selectedMonth]);

  const costMoneyData = Array.isArray(costMoneyDetail) ? costMoneyDetail : [];
  const incomeMoneyData = Array.isArray(incomeMoneyDetail) ? incomeMoneyDetail : [];
  const totalCostSum = costMoneyData.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0);

  const barData = [
    { name: "成本", value: total_cost },
    { name: "收入", value: total_income },
  ];
  const pieData = [
    { name: "有病蟲害", value: pest_count },
    { name: "無病蟲害", value: (record_count || 0) - (pest_count || 0) },
  ];
  const COLORS = ["#E53E3E", "#38A169", "#F6AD55", "#4299E1", "#9F7AEA", "#48BB78", "#ED8936"];
  const pestTrendData = Array.isArray(daily_pest_counts) ? daily_pest_counts : [];

  const isMobile = typeof window !== "undefined" && window.innerWidth < 640;

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <div className="flex-1 p-4 md:p-6 overflow-auto">
        <div className="flex items-center justify-center mb-4">
          <button
            onClick={handlePrevMonth}
            className="w-10 h-5 text-#c0d65b rounded flex items-center justify-center mr-2"
            style={{ backgroundColor: "rgba(224, 223, 223, 0.84)" }}
          >
            ←
          </button>
          <span className="font-semibold">{selectedMonth}</span>
          <button
            onClick={handleNextMonth}
            className="w-10 h-5 text-#c0d65b rounded flex items-center justify-center ml-2"
            style={{ backgroundColor: "rgba(224, 223, 223, 0.84)" }}
          >
            →
          </button>
        </div>
        <h1 className="text-3xl font-bold mb-4 text-[#c0d65b] tracking-wide text-center">本月數據總覽</h1>


        {/* 三大指標卡片 */}
        <div className="flex gap-4 mb-6">
          {["income", "cost", "pest"].map((key) => {
            const item = indicators[key] || { value: 0, pct: null };
            const title = key === "income" ? "總收入" : key === "cost" ? "總成本" : "病蟲害";
            const pctText = item.pct === null ? "N/A" : `${item.pct > 0 ? "+" : ""}${item.pct}%`;
            const colorClass = item.pct === null ? "" : item.pct > 0 ? "text-green-500" : "text-red-500";
            // income 顯示 total_income、cost 顯示 total_cost、pest 顯示 pest_count，否則 item.value
            let displayValue;
            if (key === "income") {
              displayValue = total_income;
            } else if (key === "cost") {
              displayValue = total_cost;
            } else if (key === "pest") {
              displayValue = pest_count;
            } else {
              displayValue = item.value;
            }
            return (
              <div key={key} className="bg-white rounded-xl shadow p-4 w-full">
                <h3 className="font-semibold text-[#db5343] mb-1">{title}</h3>
                <p className="text-2xl">{displayValue}</p>
                <p className={`mt-1 ${colorClass}`}>{pctText}</p>
              </div>
            );
          })}
        </div>

        {/* 異常警示 */}
        {Array.isArray(alerts) && alerts.length > 0 && (
          <div className="bg-red-100 p-4 rounded-xl shadow mb-6">
            <h4 className="font-semibold text-[#db5343] mb-2">⚠️ 本月異常警示</h4>
            <ul className="list-disc list-inside text-sm">
              {alerts.map((msg, i) => (
                <li key={i}>{msg}</li>
              ))}
            </ul>
          </div>
        )}

        {/* 月報摘要 */}
        <div className="bg-white p-4 rounded-xl shadow mb-6">
          <h4 className="font-semibold text-[#db5343] mb-2">本月農務摘要</h4>
          <p className="text-sm whitespace-pre-wrap">{summary || "無摘要資料"}</p>
        </div>

        {/* 成本 vs 收入 卡片 */}
        <div className="bg-white rounded-xl shadow p-4 mb-6 w-full">
          <h2 className="text-lg font-semibold text-[#db5343] mb-2">
            成本 vs 收入
          </h2>
          <p className="text-sm text-gray-500 mb-4">呈現本月農務相關的總成本與總收入，幫助評估收益情況。</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#c0d65b" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 病蟲害比率 卡片 */}
        <div className="bg-white rounded-xl shadow p-4 mb-6 w-full">
          <h2 className="text-lg font-semibold text-[#db5343] mb-2">
            病蟲害比率
          </h2>
          <p className="text-sm text-gray-500 mb-4">比較有病蟲害與無病蟲害的紀錄數量，用以監控田間健康。</p>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {pieData.map((entry, idx) => (
                  <Cell key={`cell-${idx}`} fill={COLORS[idx]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* 各成本來源總花費比例 卡片 */}
        <div className="bg-white rounded-xl shadow p-4 mb-6 w-full relative">
          <h2 className="text-lg font-semibold text-[#db5343] mb-2">
            各成本來源總花費比例
          </h2>
          <p className="text-sm text-gray-500 mb-4">
            各成本分類的總花費分布（單位：元）。
          </p>
          {totalCostSum > 0 ? (
            <ResponsiveContainer width="100%" height={isMobile ? 180 : 250}>
              <PieChart>
                <Pie
                  data={costMoneyData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={isMobile ? 50 : 80}
                  label={({ name, value, percent }) => `${name}：${value}元 (${(
                    percent * 100
                  ).toFixed(1)}%)`}
                >
                  {costMoneyData.map((entry, idx) => (
                    <Cell
                      key={`cost-money-cell-${idx}`}
                      fill={COLORS[idx % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
              <div
                className="absolute bottom-3 right-3 flex flex-col bg-white bg-opacity-90 rounded px-2 py-1 shadow text-xs z-10"
                style={{ pointerEvents: "none" }}
              >
                {costMoneyData.map((entry, idx) => (
                  <div
                    key={entry.name}
                    className="flex items-center mb-0.5 last:mb-0"
                  >
                    <span
                      className="inline-block w-3 h-3 rounded-sm mr-2"
                      style={{
                        backgroundColor: COLORS[idx % COLORS.length],
                      }}
                    />
                    {entry.name}
                  </div>
                ))}
              </div>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-sm text-gray-400">
              尚無成本金額資料
            </p>
          )}
        </div>

        {/* 收入來源比例 卡片 */}
        <div className="bg-white rounded-xl shadow p-4 mb-6 w-full relative">
          <h2 className="text-lg font-semibold text-[#db5343] mb-2">
            收入來源比例
          </h2>
          <p className="text-sm text-gray-500 mb-4">
            依據 Notion 中「銷售方式」欄位，自動統計各種收入來源的比例。
          </p>
          {incomeMoneyData.length > 0 ? (
            <ResponsiveContainer width="100%" height={isMobile ? 180 : 250}>
              <PieChart>
                <Pie
                  data={incomeMoneyData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={isMobile ? 50 : 80}
                  label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
                >
                  {incomeMoneyData.map((entry, idx) => (
                    <Cell
                      key={`income-detail-cell-${idx}`}
                      fill={COLORS[idx % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-sm text-gray-400">
              尚無收入來源資料
            </p>
          )}
          {incomeMoneyData.length > 0 && (
            <div
              className="absolute bottom-3 right-3 flex flex-col bg-white bg-opacity-90 rounded px-2 py-1 shadow text-xs z-10"
              style={{ pointerEvents: "none" }}
            >
              {incomeMoneyData.map((entry, idx) => (
                <div
                  key={entry.name}
                  className="flex items-center mb-0.5 last:mb-0"
                >
                  <span
                    className="inline-block w-3 h-3 rounded-sm mr-2"
                    style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                  />
                  {entry.name}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* 病蟲害細分類 卡片 */}
<div className="bg-white rounded-xl shadow p-4 mb-6 w-full relative">
  <h2 className="text-lg font-semibold text-[#db5343] mb-2">
    病蟲害細分類
  </h2>
  <p className="text-sm text-gray-500 mb-4">
    依據 Notion 中「異常狀態」欄位，統計各病蟲害次數。
  </p>
  {pest_detail.length > 0 ? (
    <ResponsiveContainer width="100%" height={isMobile ? 180 : 250}>
      <PieChart>
        <Pie
          data={pest_detail}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={isMobile ? 50 : 80}
          label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
        >
          {pest_detail.map((entry, idx) => (
            <Cell
              key={`pest-detail-cell-${idx}`}
              fill={COLORS[idx % COLORS.length]}
            />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
      <div
        className="absolute bottom-3 right-3 flex flex-col bg-white bg-opacity-90 rounded px-2 py-1 shadow text-xs z-10"
        style={{ pointerEvents: "none" }}
      >
        {pest_detail.map((entry, idx) => (
          <div
            key={entry.name}
            className="flex items-center mb-0.5 last:mb-0"
          >
            <span
              className="inline-block w-3 h-3 rounded-sm mr-2"
              style={{
                backgroundColor: COLORS[idx % COLORS.length],
              }}
            />
            {entry.name}
          </div>
        ))}
      </div>
    </ResponsiveContainer>
  ) : (
    <p className="text-center text-sm text-gray-400">
      尚無病蟲害細分類資料
    </p>
  )}
</div>

        {/* 病蟲害防治建議 區塊 */}
        <section className="bg-white rounded-xl shadow p-4 mb-6 w-full">
          <h2 className="text-lg font-semibold text-[#db5343] mb-2">
            病蟲害防治建議
          </h2>
          {pestAdvice.length > 0 ? (
            <ul className="list-disc list-inside space-y-2">
              {pestAdvice.map((item, idx) => (
                <li key={idx}>
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {item.title}
                  </a>
                  <p className="text-sm text-gray-600">{item.description}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 mt-2">本月暫無病蟲害或無建議。</p>
          )}
        </section>

      </div>
    </div>
  );
};

export default Dashboard;