import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="AI스캐너 통합 관리자 대시보드",
    page_icon="📊",
    layout="wide"
)

# 2. 구글 시트 데이터 로드 전용 함수 (60초 캐싱)
@st.cache_data(ttl=60)
def load_sheet_data(sheet_name, sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    return pd.read_csv(url)

# 🚨 본인의 구글 시트 ID를 입력해 주세요 🚨
# 구글 시트 URL 중 https://docs.google.com/spreadsheets/d/ [이부분이_시트ID] /edit 에서 가져온 값
GOOGLE_SHEET_ID = "여기에_구글시트_ID_입력"

st.title("📊 AI스캐너 실시간 통합 관리자")
st.caption("구글 시트 기반 실시간 수납 및 가맹점 CMS 매칭 데이터 대시보드입니다.")

# 3. 탭 메뉴 세팅
tab1, tab2 = st.tabs(["💳 수납(입금) 관리", "🏪 가맹점 CMS 매칭 DB"])

# --- [탭 1] 수납(입금) 관리 ---
with tab1:
    st.subheader("💳 월별 수납 및 입금 현황")
    try:
        df_pay = load_sheet_data("수납내역", GOOGLE_SHEET_ID)
        
        # 숫자 컬럼 쉼표/숫자 변환 처리
        if '수납금액' in df_pay.columns:
            df_pay['수납금액_num'] = pd.to_numeric(df_pay['수납금액'].astype(str).str.replace(r'[^0-9]', '', regex=True), errors='coerce').fillna(0)
        else:
            df_pay['수납금액_num'] = 0

        total_count = len(df_pay)
        total_pay = int(df_pay['수납금액_num'].sum())
        total_supply = int(total_pay / 1.1)

        # KPI 카드 표시
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("총 수납 건수", f"{total_count:,} 건")
        kpi2.metric("총 수납 금액 (VAT 포함)", f"{total_pay:,} 원")
        kpi3.metric("총 공급가액 (VAT 제외)", f"{total_supply:,} 원")
        
        st.divider()
        st.markdown("### 📑 수납 상세 내역 리스트")
        st.dataframe(df_pay.drop(columns=['수납금액_num'], errors='ignore'), use_container_width=True)

    except Exception as e:
        st.warning("⚠️ 구글 시트의 '수납내역' 탭 데이터를 읽어올 수 없습니다. 시트 ID와 [웹에 게시] 상태를 확인해주세요.")

# --- [탭 2] 가맹점 CMS 매칭 DB ---
with tab2:
    st.subheader("🏪 가맹점 - 회원번호 매칭 정보 (CMS)")
    try:
        df_cms = load_sheet_data("CMS", GOOGLE_SHEET_ID)
        st.dataframe(df_cms, use_container_width=True)
    except Exception as e:
        st.warning("⚠️ 구글 시트의 'CMS' 탭 데이터를 읽어올 수 없습니다. 시트 ID와 [웹에 게시] 상태를 확인해주세요.")
