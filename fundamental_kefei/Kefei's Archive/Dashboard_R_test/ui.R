library(shiny)
library(shinydashboard)
library(ggplot2)
library(readr)
library(plotly)
library(shinythemes)

constituent_list = c('Allianz', 'BASF', 'BMW', 'Bayer', 'Beiersdorf',
'Commerzbank', 'Continental', 'Daimler',
'Deutsche Bank', 'Deutsche Börse', 'Deutsche Post',
'Deutsche Telekom', 'EON', 'Fresenius',
'Fresenius Medical Care', 'Henkel', 'Infineon', 'Linde',
'Lufthansa', 'Merck', 'ProSiebenSat1 Media', 'RWE', 'SAP',
'Siemens', 'Vonovia', 'Adidas', 'Thyssenkrupp','Volkswagen')


ui <- dashboardPage(
  dashboardHeader( 
    title = 'iGenie Analytics'),
  dashboardSidebar(
    sidebarMenu(
      #actionButton(inputId = "reload", label = "Refresh",icon=icon('refresh'),width='85%'),
      menuItem("Homepage", tabName = "dashboard", icon = icon("dashboard")),
      menuItem("Market & Analysts", tabName = "analyst_prediction", icon = icon("th")),
      menuItem("Fundamental", tabName = "fundamental_analysis", icon = icon("th")),
      selectInput("constituent", "Select a constituent:", 
                    choices=constituent_list,
        helpText("Select Constituent")),
      menuItem("Twitter Sentiment", tabName = "twitter_analysis", icon = icon("th")),
      menuItem("News Sentiment", tabName = "news_analysis", icon = icon("th")),
      menuItem("Price vs. Sentiment", tabName = "correlation", icon = icon("th"))
    )
  ),
  
  dashboardBody(
    tabItems(
      ############################ HOMEPAGE ####################################
      tabItem(tabName='dashboard',
              fluidRow(
                tabBox(title = 'Tweets',
                       side = 'right',
                       id = 'tabset1',height='550px',
                       tabPanel("All",
                                plotOutput('popular_treemap',height = '420px', width = '100%'))
                ),
                
                ##implement some sort of auto-height
                tabBox( title = 'News',
                        side='right',
                        id='tabset1',height='550px',
                        tabPanel('All',
                                 DT::dataTableOutput('news_all'))
                        
                )
              ),
              
              
              fluidRow(
                tabBox(
                  #display analyst recommendation, and perhaps target prices
                  title = "Analyst Recommendation",
                  id='tabset1',
                  side='right',
                  height=550,
                  #status = 'primary',
                  tabPanel('L-V',
                           plotOutput("analystplot3", height = 490, width = '100%')
                  ),
                  tabPanel('D-L',
                           plotOutput("analystplot2", height = 490, width = '100%')
                  ),
                  tabPanel('A-D',
                           plotOutput("analystplot1", height = 490, width = '100%')
                           )
                  
                ),
                
                tabBox(
                  #display the color coded box
                  height=550,
                  title = "Summary",
                  side='right',
                  #status = 'primary',
                  tabPanel('L-V',
                           DT::dataTableOutput('summarytable3')),
                  tabPanel('D-L',
                           DT::dataTableOutput('summarytable2')),
                  tabPanel('A-D',
                           DT::dataTableOutput('summarytable1'))
                  
                )
              )
      ),
      
      ############################ FUNDAMENTAL PAGE ####################################
      tabItem(tabName = 'fundamental_analysis',
              fluidRow(
                box(title='Profitability Ranking',
                    height=600,
                    align='center',
                    DT:: dataTableOutput('ranking_top')
                ),
                
                
                box(title='Cumulative Return',
                    height=600,
                    align='center',
                    #status = 'primary',
                    DT::dataTableOutput('CRtable')
                )),
              
              fluidRow(
                box(title= 'Earning per Share',
                    height=400,
                    align='center',
                    DT::dataTableOutput('EPS_table')
                ),
                
                
                box(title='Price/Earning Ratio',
                    height=400,
                    align='center',
                    DT::dataTableOutput('PER_table')    
                ))
      ),
      
      ############################ ANALYST PAGE ####################################
      tabItem(tabName = 'analyst_prediction',
              fluidRow(
                box(title= 'Analyst Recommendation',
                    height=600,
                    align='center',
                    DT::dataTableOutput('recommendation_table') 
                ),
                box(title='Target Prices',
                    height=600,
                    align='center',
                    DT::dataTableOutput('target_price_table') 
                )
              )
              
              
      ),
      
      
      ############################ NEWS PAGE ####################################
      tabItem(tabName = 'news_analysis',
              fluidRow(
                box(title= 'News Tagging',
                    height=500,
                    plotOutput('news_tag_bar') 
                ),
                box(title='News Top Words',
                    height=500,
                    plotOutput('word_cloud') 
                )
              ),
              
              #news_sentiment_tag
              fluidRow(
                box(title='News Sentiment Trend',
                    height=500,
                    plotOutput('news_sentiment_daily',height=400)
                ),
                
                box(title='News Sentiment Analysis by Category',
                    height=500,
                    plotOutput('news_sentiment_tag',height=400)
                )
              )
      ),
      
      ############################ CORRELATION PAGE ####################################
      tabItem(tabName = 'correlation',
              fluidRow(
                
                box(title='News Sentiment vs. Stock Price Behavior',
                    height=620,
                    plotlyOutput('news_behavior_line',height="80%"),
                    h6("   "),
                    textOutput('news_annotation')
                ),
                
                box(title='Twitter Sentiment vs. Stock Price Behavior',
                    height=620,
                    plotlyOutput('twitter_behavior_line',height="80%"),
                    h6("    "),
                    textOutput('twitter_annotation')
                )
              )
              
      ),
      
      ############################ TWITTER PAGE ####################################
      tabItem(tabName = 'twitter_analysis',
              fluidRow(
                tabBox(title=h4("Twitter Target Price"), height=500,side='right',
                       tabPanel('General',
                                plotOutput("twitter_target_price", height=420)),
                       
                       tabPanel('Influencer',
                                plotOutput("influencer_target_price", height=420))),
                
                tabBox(title = h4('Twitter Analysis by Countries'),height=500,side='right',
                       tabPanel('Sentiment',
                                plotOutput('sentiment_map',height=400)),
                       tabPanel('Frequency',
                                plotOutput('popularity_map',height=400)))),
              
              
              fluidRow(  
                box(title='Twitter Sentiment Count',
                    align='center',
                    plotOutput('tweet_num',height=400),
                    height=500),
                
                box(title='Top Words Mentioned ',
                    align='center',
                    plotOutput('organization',height=400),
                    height=500))
      )
    )
  )
)




