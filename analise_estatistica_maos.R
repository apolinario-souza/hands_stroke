# =============================================================================
# ANÁLISE DE MODELOS LINEARES MISTOS (LMM)
# Estudo de movimentos de mão em pacientes com AVC
# Efeitos fixos: lesion (NS/LS/RS) x hand (LH/RH)
# Efeito aleatório: sujeito (sub)
# =============================================================================
setwd("C:/Users/lemeu/master_daiana")

# --- 1. Pacotes necessários ---------------------------------------------------
library(readxl)
library(tidyverse)
library(lme4)
library(lmerTest)    # p-valores via aproximação Satterthwaite
library(emmeans)     # contrastes e comparações post-hoc
library(performance) # diagnóstico do modelo
library(car)         # Anova tipo III
library(ggplot2)
library(knitr)


# --- 2. Leitura e preparo dos dados ------------------------------------------
# Os dados agora estão organizados em abas separadas dentro de data.xlsx.
# Cada aba corresponde a uma variável dependente e contém as colunas:
#   sub | lesion | valor | hand
# O código abaixo lê todas as abas e combina em um único data frame no
# formato longo, recriando as colunas "variable" e "value" usadas antes.

arquivo <- "data.xlsx"
abas    <- excel_sheets(arquivo)

df <- map_dfr(abas, function(aba) {
  d <- read_excel(arquivo, sheet = aba)
  d <- d[ , c("sub", "lesion", "hand", "valor")]   # seleciona colunas relevantes
  names(d)[names(d) == "valor"] <- "value"          # renomeia "valor" → "value"
  d$variable <- aba                                 # nome da aba vira a variável
  d
})

# Converter variáveis categóricas em fatores
df <- df %>%
  mutate(
    sub      = factor(sub),
    lesion   = factor(lesion, levels = c("NS", "LS", "RS")),  # NS como referência
    hand     = factor(hand,   levels = c("LH", "RH")),
    variable = factor(variable)
  )

# Verificar estrutura
glimpse(df)
cat("\nDistribuição por lesão e mão:\n")
table(df$lesion, df$hand)


# --- 3. Função: rodar LMM para uma variável ----------------------------------

rodar_lmm <- function(variavel, dados) {
  
  cat("\n")
  cat(strrep("=", 70), "\n")
  cat("VARIÁVEL:", variavel, "\n")
  cat(strrep("=", 70), "\n")
  
  d <- dados %>% filter(variable == variavel) %>% droplevels()
  
  formula_mod <- value ~ lesion * hand + (1 | sub)
  
  modelo <- tryCatch(
    lmer(formula_mod, data = d, REML = TRUE,
         control = lmerControl(optimizer = "bobyqa")),
    error = function(e) {
      cat("  ERRO ao ajustar modelo:", conditionMessage(e), "\n")
      return(NULL)
    }
  )
  
  if (is.null(modelo)) return(invisible(NULL))
  
  # --- Tabela ANOVA tipo III (graus de liberdade Satterthwaite) ---
  cat("\n>> ANOVA Tipo III (Satterthwaite):\n")
  aov_tab <- anova(modelo, type = "III")
  print(aov_tab)
  
  # --- Estimativas dos efeitos fixos ---
  cat("\n>> Coeficientes do modelo:\n")
  print(summary(modelo)$coefficients)
  
  # --- Variância dos efeitos aleatórios ---
  cat("\n>> Variância do efeito aleatório (sujeito):\n")
  print(as.data.frame(VarCorr(modelo)))
  
  # --- Post-hoc: médias marginais e comparações ---
  cat("\n>> Médias marginais estimadas (lesion x hand):\n")
  emm <- emmeans(modelo, ~ lesion * hand)
  print(emm)
  
  cat("\n>> Contrastes entre grupos de lesão (por mão):\n")
  contraste_lesion <- emmeans(modelo, pairwise ~ lesion | hand,
                              adjust = "tukey")
  print(contraste_lesion$contrasts)
  
  cat("\n>> Contraste entre mãos (por grupo de lesão):\n")
  contraste_hand <- emmeans(modelo, pairwise ~ hand | lesion,
                            adjust = "tukey")
  print(contraste_hand$contrasts)
  
  # Post-hoc quando interação NÃO é significativa
  cat("\n>> Contraste entre os grupos (colapsando sobre mão):\n")
  contraste_lesion2 <- emmeans(modelo, pairwise ~ lesion, adjust = "tukey")
  print(contraste_lesion2$contrasts)
  
  cat("\n>> Contraste entre as mãos (colapsando sobre lesão):\n")
  contraste_hand2 <- emmeans(modelo, pairwise ~ hand, adjust = "tukey")
  print(contraste_hand2$contrasts)
  
  # --- Diagnóstico básico ---
  cat("\n>> R² do modelo:\n")
  r2 <- performance::r2(modelo)
  print(r2)
  
  return(invisible(modelo))
}


# --- 4. Rodar para todas as variáveis ----------------------------------------

variaveis <- levels(df$variable)

resultados <- list()
for (v in variaveis) {
  resultados[[v]] <- rodar_lmm(v, df)
}


# --- 5. Salvar resultados em Markdown ----------------------------------------

sink_md <- function(dados, variaveis, arquivo_saida = "resultados_LMM.md") {
  
  con <- file(arquivo_saida, open = "wt", encoding = "UTF-8")
  
  writeLines("# Resultados — Modelos Lineares Mistos\n", con)
  writeLines(paste("**Data:**", format(Sys.time(), "%d/%m/%Y %H:%M"), "\n"), con)
  writeLines("**Modelo:** `value ~ lesion * hand + (1 | sub)`  \n", con)
  writeLines("**Efeito aleatório:** sujeito (`sub`)  \n", con)
  writeLines("---\n", con)
  
  for (v in variaveis) {
    
    d <- dados %>% filter(variable == v) %>% droplevels()
    
    modelo <- tryCatch(
      lmer(value ~ lesion * hand + (1 | sub), data = d, REML = TRUE,
           control = lmerControl(optimizer = "bobyqa")),
      error = function(e) NULL
    )
    
    if (is.null(modelo)) next
    
    writeLines(paste0("## ", v, "\n"), con)
    
    # ANOVA tipo III
    writeLines("### ANOVA Tipo III (Satterthwaite)\n", con)
    aov_tab <- as.data.frame(anova(modelo, type = "III"))
    writeLines(knitr::kable(aov_tab, format = "markdown", digits = 4), con)
    writeLines("\n", con)
    
    p_interacao <- aov_tab["lesion:hand", "Pr(>F)"]
    p_lesion    <- aov_tab["lesion",      "Pr(>F)"]
    p_hand      <- aov_tab["hand",        "Pr(>F)"]
    
    if (!is.na(p_interacao) && p_interacao < 0.05) {
      
      writeLines("### Post-hoc: Efeitos Simples (interação significativa)\n", con)
      
      c1 <- emmeans(modelo, pairwise ~ lesion | hand, adjust = "tukey")
      writeLines("#### Lesão por mão\n", con)
      writeLines(knitr::kable(as.data.frame(c1$contrasts),
                              format = "markdown", digits = 4), con)
      writeLines("\n", con)
      
      c2 <- emmeans(modelo, pairwise ~ hand | lesion, adjust = "tukey")
      writeLines("#### Mão por lesão\n", con)
      writeLines(knitr::kable(as.data.frame(c2$contrasts),
                              format = "markdown", digits = 4), con)
      writeLines("\n", con)
    }
    
    if (!is.na(p_lesion) && p_lesion < 0.05) {
      writeLines("### Post-hoc: Efeitos Principais (interação não significativa)\n", con)
      
      c1 <- emmeans(modelo, pairwise ~ lesion, adjust = "tukey")
      writeLines("#### Comparação entre grupos de lesão\n", con)
      writeLines(knitr::kable(as.data.frame(c1$contrasts),
                              format = "markdown", digits = 4), con)
      writeLines("\n", con)
    }
    
    if (!is.na(p_hand) && p_hand < 0.05) {
      c2 <- emmeans(modelo, pairwise ~ hand, adjust = "tukey")
      writeLines("#### Comparação entre mãos\n", con)
      writeLines(knitr::kable(as.data.frame(c2$contrasts),
                              format = "markdown", digits = 4), con)
      writeLines("\n", con)
    }
    
    # R²
    var_fixo     <- var(as.numeric(fitted(modelo)))
    var_residual <- sigma(modelo)^2
    var_alea     <- as.numeric(VarCorr(modelo)$sub)
    r2_m <- var_fixo / (var_fixo + var_alea + var_residual)
    r2_c <- (var_fixo + var_alea) / (var_fixo + var_alea + var_residual)
    
    writeLines("### R²\n", con)
    writeLines(knitr::kable(
      data.frame(R2_marginal = round(r2_m, 3), R2_condicional = round(r2_c, 3)),
      format = "markdown"), con)
    writeLines("\n---\n", con)
  }
  
  close(con)
  cat("Resultados salvos em:", arquivo_saida, "\n")
}

sink_md(df, variaveis)