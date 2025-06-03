import React, { useEffect, useState } from "react";
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
  const [data, setData] = useState(null);
  const [selectedMonth, setSelectedMonth] = useState("2025-06");

  const handlePrevMonth = () => {
    setSelectedMonth(prevMonth(selectedMonth));
  };

  const handleNextMonth = () => {
    const date = new Date(selectedMonth + "-01");
    date.setMonth(date.getMonth() + 1);
    setSelectedMonth(date.toISOString().slice(0, 7));
  };

  useEffect(() => {
    fetch(`http://localhost:5003/api/dashboard?month=${selectedMonth}`)
      .then((res) => res.json())
      .then((json) => {
        console.log(json);
        setData(json);
      });
  }, [selectedMonth]);

  // Normalize cost_money_detail into an array of { name, value }
  const costMoneyData = Array.isArray(data?.cost_money_detail)
    ? data.cost_money_detail
    : Object.entries(data?.cost_money_detail || {}).map(([name, value]) => ({ name, value }));
  const totalCostSum = costMoneyData.reduce((sum, entry) => sum + (Number(entry.value) || 0), 0);

  if (!data) return <p className="text-center mt-8">資料載入中…</p>;

  const isMobile = typeof window !== "undefined" && window.innerWidth < 640;
  const costLabelOk = data.cost_detail.length <= 5;
  const incomeLabelOk = data.income_detail.length <= 5;

  const barData = [
    { name: "成本", value: data?.total_cost || 0 },
    { name: "收入", value: data?.total_income || 0 },
  ];
  const pieData = [
    { name: "有病蟲害", value: data?.pest_count || 0 },
    { name: "無病蟲害", value: (data?.record_count || 0) - (data?.pest_count || 0) },
  ];
  const COLORS = ["#E53E3E", "#38A169", "#F6AD55", "#4299E1", "#9F7AEA", "#48BB78", "#ED8936"];
  const pestTrendData = data.daily_pest_counts || [];

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* Main Content */}
      <div className="flex-1 p-4 md:p-6 overflow-auto">
        <div className="flex items-center mb-4">
          <button
            onClick={handlePrevMonth}
            className="px-3 py-1 bg-[#c9403e] text-white rounded hover:bg-[#a63e3e] mr-2"
          >
            ← 上個月
          </button>
          <span className="font-semibold">{selectedMonth}</span>
          <button
            onClick={handleNextMonth}
            className="px-3 py-1 bg-[#c9403e] text-white rounded hover:bg-[#a63e3e] ml-2"
          >
            下個月 →
          </button>
        </div>
        <h1 className="text-3xl font-bold mb-4 text-[#c9403e] tracking-wide">本月數據總覽</h1>

        {/* AI 數據摘要分析 */}
        {data.ai_summary && (
          <div className="bg-yellow-50 p-4 rounded shadow mb-6">
            <h2 className="text-lg font-semibold text-[#db5343] mb-2">
              AI 數據摘要分析
            </h2>
            <p className="text-sm mb-1">
              <strong>{selectedMonth}：</strong>{data.ai_summary[selectedMonth]}
            </p>
            <p className="text-sm">
              <strong>{prevMonth(selectedMonth)}：</strong>{data.ai_summary[prevMonth(selectedMonth)]}
            </p>
          </div>
        )}

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
                  label={({ name, value, percent }) => `${name}：${value}元 (${(percent * 100).toFixed(1)}%)`}
                >
                  {costMoneyData.map((entry, idx) => (
                    <Cell key={`cost-money-cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
              {/* Custom legend for cost_money_detail */}
              <div
                className="absolute bottom-3 right-3 flex flex-col bg-white bg-opacity-90 rounded px-2 py-1 shadow text-xs z-10"
                style={{ pointerEvents: "none" }}
              >
                {costMoneyData.map((entry, idx) => (
                  <div key={entry.name} className="flex items-center mb-0.5 last:mb-0">
                    <span
                      className="inline-block w-3 h-3 rounded-sm mr-2"
                      style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                    />
                    {entry.name}
                  </div>
                ))}
              </div>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-sm text-gray-400">尚無成本金額資料</p>
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
          {data.income_detail && data.income_detail.length > 0 ? (
            <ResponsiveContainer width="100%" height={isMobile ? 180 : 250}>
              <PieChart>
                <Pie
                  data={data.income_detail}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={isMobile ? 50 : 80}
                  label={({ percent }) => `${(percent * 100).toFixed(1)}%`}
                >
                  {data.income_detail.map((entry, idx) => (
                    <Cell key={`income-detail-cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-sm text-gray-400">尚無收入來源資料</p>
          )}
          {/* Custom legend for income_detail */}
          {data.income_detail && data.income_detail.length > 0 && (
            <div
              className="absolute bottom-3 right-3 flex flex-col bg-white bg-opacity-90 rounded px-2 py-1 shadow text-xs z-10"
              style={{ pointerEvents: "none" }}
            >
              {data.income_detail.map((entry, idx) => (
                <div key={entry.name} className="flex items-center mb-0.5 last:mb-0">
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
            病蟲害細分類統計
          </h2>
          <p className="text-sm text-gray-500 mb-4">依據 Notion 中「異常狀態」欄位統計各種病蟲害的出現頻率，幫助後續防治與管理。</p>
          {data.pest_detail && data.pest_detail.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={data.pest_detail}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  label
                >
                  {data.pest_detail.map((entry, idx) => (
                    <Cell key={`detail-cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-sm text-gray-400">尚無細分類資料</p>
          )}
        </div>

        {/* 每日記錄次數 卡片 */}
        <div className="bg-white rounded-xl shadow p-4 mb-6 w-full">
          <h2 className="text-lg font-semibold text-[#db5343] mb-2">
            每日記錄次數
          </h2>
          <p className="text-sm text-gray-500 mb-4">顯示每天記錄筆數，協助觀察農務紀錄的頻率與規律。</p>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data.daily_counts || []}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#3182CE" />
            </BarChart>
          </ResponsiveContainer>
        </div>


        {/* 統計數字 卡片 */}
        <div className="bg-white rounded-xl shadow p-4 max-w-md mx-auto w-full">
          <p className="text-gray-700 mb-2">
            本月共記錄：
            <span className="font-bold"> {data.record_count} 筆</span>
          </p>
          <p className="text-gray-700 mb-2">
            病蟲害筆數：
            <span className="text-[#db5343] font-bold"> {data.pest_count}</span>
          </p>
          <p className="text-gray-700 mb-2">
            本月總成本：
            <span className="text-[#386641] font-bold"> {data.total_cost} 元</span>
          </p>
          <p className="text-gray-700">
            本月總收入：
            <span className="text-[#386641] font-bold"> {data.total_income} 元</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;